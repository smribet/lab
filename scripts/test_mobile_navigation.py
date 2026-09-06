"""Browser regression checks against the static export.

Run after `myst build --html`:
    uv run --with playwright python scripts/test_mobile_navigation.py
Requires Playwright's Chromium and WebKit browsers to be installed.
"""

import argparse
import asyncio
import traceback
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.async_api import async_playwright


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


async def touch(page, locator):
    # Dispatch real touch input without relying on page animation callbacks,
    # which Chromium can stop scheduling when JavaScript is disabled.
    await locator.wait_for(state="visible")
    box = await locator.bounding_box()
    assert box and box["width"] >= 44 and box["height"] >= 44
    point = {"x": box["x"] + box["width"] / 2, "y": box["y"] + box["height"] / 2}
    assert await locator.evaluate(
        "(el, p) => el.contains(document.elementFromPoint(p.x, p.y))", point
    )
    await page.touchscreen.tap(**point)


async def check(browser, base_url):
    async def local_assets_only(route):
        # Third-party notebook styles are unrelated to navigation. Keep this
        # regression test deterministic when those CDNs are unavailable.
        if not route.request.url.startswith(base_url):
            await route.fulfill(status=200, body="", content_type="text/css")
        else:
            await route.continue_()

    print("Checking navigation with JavaScript disabled", flush=True)
    device = dict(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    context = await browser.new_context(**device, java_script_enabled=False)
    context.set_default_timeout(10000)
    await context.route("**/*", local_assets_only)
    page = await asyncio.wait_for(context.new_page(), timeout=15)
    await page.goto(base_url)
    menu = page.locator("details.nbc-mobile-menu")
    await touch(page, menu.locator(":scope > summary"))
    assert await menu.evaluate("el => el.open")
    await touch(page, menu.get_by_text("Resources", exact=True))
    print("Following Gallery without JavaScript", flush=True)
    await touch(page, menu.get_by_role("link", name="Gallery", exact=True))
    await page.wait_for_url("**/gallery/")
    await touch(page, page.locator(".nbc-mobile-menu-toggle"))
    await touch(page, page.locator(".nbc-mobile-menu").get_by_role("link", name="Team", exact=True))
    await page.wait_for_url("**/team/")
    await context.close()

    print("Checking navigation while app scripts are delayed", flush=True)
    context = await browser.new_context(**device)
    context.set_default_timeout(10000)
    await context.add_init_script(
        "document.addEventListener('nbc:hydrated', () => window.testHydrated = true)"
    )
    page = await context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("console", lambda msg: errors.append(msg.text)
            if msg.type == "error" and "integrity" not in msg.text else None)
    scripts_ready = asyncio.Event()

    async def delay_scripts(route):
        if not route.request.url.startswith(base_url):
            return await route.fulfill(status=200, body="", content_type="text/css")
        if route.request.resource_type == "script":
            try:
                await asyncio.wait_for(scripts_ready.wait(), timeout=20)
            except asyncio.TimeoutError:
                pass
        await route.continue_()

    await page.route("**/*", delay_scripts)
    await page.goto(base_url, wait_until="commit")
    menu = page.locator("details.nbc-mobile-menu")
    toggle = page.locator(".nbc-mobile-menu-toggle")
    await toggle.tap()
    await menu.get_by_text("Resources", exact=True).tap()
    assert await menu.evaluate("el => el.open")
    assert not await page.evaluate("!!window.testHydrated")
    assert await menu.get_by_role("link", name="Gallery", exact=True).is_visible()
    assert await page.evaluate(
        "document.documentElement.scrollWidth <= window.innerWidth"
    )
    panel = await page.locator(".nbc-mobile-menu-panel").bounding_box()
    header = await page.locator(".myst-top-nav").bounding_box()
    assert panel["y"] >= header["y"] + header["height"] - 1
    assert panel["y"] + panel["height"] <= 844

    # Hydrating while both native disclosures are open must preserve their
    # state and must not report mismatched server/client markup.
    scripts_ready.set()
    print("Checking hydration with the menu open", flush=True)
    await page.wait_for_function("window.testHydrated", timeout=30000)
    assert await menu.evaluate("el => el.open")
    assert await menu.get_by_role("link", name="Gallery", exact=True).is_visible()
    await page.keyboard.press("Escape")
    assert not await menu.evaluate("el => el.open")
    assert await toggle.evaluate("el => el === document.activeElement")
    await page.keyboard.press("Enter")
    assert await menu.evaluate("el => el.open")
    await page.touchscreen.tap(380, 700)
    assert not await menu.evaluate("el => el.open")
    await toggle.tap()
    await menu.get_by_role("link", name="Team", exact=True).tap()
    await page.wait_for_url("**/team/")
    await page.wait_for_function("window.testHydrated")
    assert not errors, errors

    # A narrow screen and a short landscape viewport must stay scrollable.
    for width, height in [(320, 568), (844, 390)]:
        await page.set_viewport_size({"width": width, "height": height})
        await toggle.tap()
        if not await menu.locator(".nbc-mobile-group").evaluate("el => el.open"):
            await menu.get_by_text("Resources", exact=True).tap()
        await menu.get_by_role("link", name="Gallery", exact=True).scroll_into_view_if_needed()
        assert await page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        panel = await page.locator(".nbc-mobile-menu-panel").bounding_box()
        assert panel["y"] + panel["height"] <= height
        await page.keyboard.press("Escape")

    await page.set_viewport_size({"width": 1280, "height": 900})
    assert not await toggle.is_visible()
    assert await page.locator(".myst-top-nav-item").get_by_role("link", name="Team").is_visible()
    assert not errors, errors
    await context.close()


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", action="append", choices=["chromium", "webkit"])
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "_build" / "html"
    assert (root / "index.html").exists(), "Run myst build --html first"
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(root)))
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        async with async_playwright() as playwright:
            for name in args.browser or ["chromium", "webkit"]:
                engine = getattr(playwright, name)
                browser = await engine.launch()
                try:
                    await asyncio.wait_for(
                        check(browser, f"http://127.0.0.1:{server.server_port}/"), timeout=90
                    )
                    print(f"PASS {engine.name}: no JS, delayed JS, hydration, touch, keyboard, desktop", flush=True)
                except BaseException:
                    traceback.print_exc()
                    raise
                finally:
                    await asyncio.wait_for(browser.close(), timeout=30)
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    asyncio.run(main())
