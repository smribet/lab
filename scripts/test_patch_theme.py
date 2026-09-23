"""Run with python3 -m unittest discover -s scripts -p test_patch_theme.py."""

import unittest

from patch_theme import navigation_helpers, patched


class ThemePatchTests(unittest.TestCase):
    def test_old_toc_hook(self):
        src = ('[s,o]=X.useState(r);(0,X.useEffect)(()=>{n.state==="idle"&&o(r)},'
               '[n.state]);let a=fn(e,i,t);return!i.children')
        result, count = patched(src)
        self.assertEqual(count, 1)
        self.assertIn('useState((i.level===1||r))', result)
        self.assertIn('o((i.level===1||r))', result)
        self.assertIn('[n.state]', result)

    def test_current_toc_recomputes_active_path(self):
        # The current upstream theme recomputes active state after navigation
        # and includes pathname in the effect dependencies.
        src = ('[s,a]=_0.default.useState(o);(0,_0.useEffect)(()=>{'
               'i.state==="idle"&&a(DS([t],e,r).includes(t.id))},[i.state,e]);'
               'let c=nD(e,t,r);return!t.children')
        result, count = patched(src)
        self.assertEqual(count, 1)
        self.assertIn('useState((t.level===1||o))', result)
        self.assertIn('a((t.level===1||DS([t],e,r).includes(t.id)))', result)
        self.assertIn('[i.state,e]', result)
        self.assertEqual(patched(result), (result, 0))

    def test_helpers_resolved_for_server_and_client(self):
        for fetcher in ('sk', '(0,Wpn.useFetcher)'):
            with self.subTest(fetcher=fetcher):
                src = ('i=Pr(),{title:s,nav:a,actions:c};'
                       '(0,ft.jsxs)("div",{className:"myst-top-nav rest"});'
                       f'let t=zt(),e={fetcher}(),[r,n]=(0,Ot.useState)(!0);'
                       'let s=Ct("/myst.search.json",t);')
                self.assertEqual(navigation_helpers(src), {
                    'NBC_JSX': 'ft', 'NBC_CONFIG': 'Pr',
                    'NBC_BASE': 'zt', 'NBC_URL': 'Ct',
                })

    def test_unknown_helpers_fail_clearly(self):
        with self.assertRaisesRegex(SystemExit, 'NBC_JSX'):
            navigation_helpers('unrecognized theme')


if __name__ == '__main__':
    unittest.main()
