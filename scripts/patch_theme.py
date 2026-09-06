"""Patch the downloaded book-theme template: keep top-level TOC sections
expanded, replace dialog search with a flat input, and repair mobile navigation.

Ported from quantem-docs. The stock theme opens a sidebar section only
while it contains the active page (and re-collapses it on navigation),
and its search opens a modal dialog. There are no template options for
either, so we patch the compiled bundles in _build/templates. Run after
the template has been downloaded (any `myst build` or `myst start` does
that), and re-run whenever _build is cleared:

    python3 scripts/patch_theme.py

The deploy workflow runs this between a warm-up build and the real build.
"""

import hashlib
import os
import re
import sys
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
THEME = os.path.normpath(
    os.path.join(HERE, "..", "_build", "templates", "site", "myst", "book-theme")
)

TARGETS = [
    os.path.join(THEME, "build", "index.js"),
    os.path.join(THEME, "public", "build", "_shared", "chunk-RUUCG5OS.js"),
]

# Flat top-bar search runtime (replaces the theme's dialog search).
# Injected into the server-rendered HTML. The search index path is
# resolved relative to the current page so it also works when the site
# is served under a path prefix (GitHub Pages project sites).
_RUNTIME = """
;(function(){
  /* ---------- flat top-bar search (replaces the theme's dialog) -------- */
  var idx=null,loading=false,waiters=[];
  function indexUrls(){
    var seg=window.location.pathname.split('/').filter(Boolean);
    var urls=['/myst.search.json'];
    if(seg.length)urls.unshift('/'+seg[0]+'/myst.search.json');
    return urls;
  }
  function load(cb){
    if(cb&&idx)return cb();
    if(cb)waiters.push(cb);
    if(idx||loading)return;
    loading=true;
    var urls=indexUrls();
    function attempt(i){
      if(i>=urls.length){loading=false;waiters=[];return;}
      fetch(urls[i]).then(function(r){
        if(!r.ok)throw new Error('http '+r.status);
        return r.json();
      }).then(function(d){
        idx=d.records||[];loading=false;
        var w=waiters;waiters=[];w.forEach(function(f){f();});
      }).catch(function(){attempt(i+1);});
    }
    attempt(0);
  }
  function titleOf(h){
    return [h.lvl3,h.lvl2,h.lvl1].filter(Boolean)[0]||'';
  }
  function crumbOf(h){
    return [h.lvl1,h.lvl2,h.lvl3].filter(Boolean).join(' > ');
  }
  function search(q){
    if(!idx)return [];
    var terms=q.toLowerCase().split(/\\s+/).filter(Boolean);
    if(!terms.length)return [];
    var seen={},out=[];
    idx.forEach(function(rec){
      var h=rec.hierarchy||{};
      var title=titleOf(h),crumb=crumbOf(h);
      var hay=(crumb+' '+(rec.content||'')).toLowerCase();
      var titleHay=crumb.toLowerCase();
      var score=0;
      for(var i=0;i<terms.length;i++){
        if(hay.indexOf(terms[i])<0)return;
        if(titleHay.indexOf(terms[i])>=0)score+=3;
        score+=1;
      }
      if(rec.type!=='content')score+=2;
      var key=rec.url;
      if(seen[key]!==undefined){
        if(out[seen[key]].score>=score)return;
        out[seen[key]]={score:score,url:rec.url,title:title,crumb:crumb,
                        content:rec.content||''};
        return;
      }
      seen[key]=out.length;
      out.push({score:score,url:rec.url,title:title,crumb:crumb,
                content:rec.content||''});
    });
    out.sort(function(a,b){return b.score-a.score;});
    return out.slice(0,8);
  }
  function build(bar){
    if(!bar||bar.dataset.nbcSearch)return;
    bar.dataset.nbcSearch='1';
    var wrap=document.createElement('div');
    wrap.className='nbc-search';
    var input=document.createElement('input');
    input.type='search';
    input.placeholder='Search';
    input.setAttribute('aria-label','Search this site');
    var list=document.createElement('div');
    list.className='nbc-search-results';
    list.hidden=true;
    wrap.appendChild(input);
    wrap.appendChild(list);
    bar.style.display='none';
    bar.after(wrap);
    var active=-1,hits=[];
    function render(){
      list.innerHTML='';
      if(!hits.length){list.hidden=true;return;}
      hits.forEach(function(h,i){
        var a=document.createElement('a');
        a.href=h.url;
        a.className='nbc-search-hit'+(i===active?' active':'');
        var t=document.createElement('div');
        t.className='nbc-search-hit-title';
        t.textContent=h.crumb||h.title;
        a.appendChild(t);
        if(h.content){
          var c=document.createElement('div');
          c.className='nbc-search-hit-text';
          c.textContent=h.content.slice(0,110);
          a.appendChild(c);
        }
        list.appendChild(a);
      });
      list.hidden=false;
    }
    function run(){
      active=-1;
      hits=search(input.value.trim());
      render();
    }
    input.addEventListener('focus',function(){load();});
    input.addEventListener('input',function(){
      load(run);   // re-runs once the index finishes loading
      run();
    });
    input.addEventListener('keydown',function(ev){
      if(ev.key==='ArrowDown'||ev.key==='ArrowUp'){
        ev.preventDefault();
        if(!hits.length)return;
        active=(active+(ev.key==='ArrowDown'?1:-1)+hits.length)%hits.length;
        render();
      }else if(ev.key==='Enter'){
        var h=hits[active<0?0:active];
        if(h){ev.preventDefault();window.location.href=h.url;}
      }else if(ev.key==='Escape'){
        input.value='';hits=[];render();input.blur();
      }
    });
    document.addEventListener('click',function(ev){
      if(!wrap.contains(ev.target)){hits=[];render();}
    });
    document.addEventListener('keydown',function(ev){
      if((ev.metaKey||ev.ctrlKey)&&ev.key.toLowerCase()==='k'){
        ev.preventDefault();ev.stopPropagation();input.focus();input.select();
      }
    },true);
  }
  function tick(){build(document.querySelector('button.myst-search-bar'));}
  function start(){
    tick();
    new MutationObserver(tick).observe(
      document.documentElement,{subtree:true,childList:true});
  }
  // Navigation uses native disclosures and links. These optional conveniences
  // run immediately; opening the menu and following links need no JavaScript.
  function menu(){return document.querySelector('details.nbc-mobile-menu');}
  document.addEventListener('click',function(ev){
    var nav=menu();
    if(nav&&nav.open&&!nav.contains(ev.target))nav.open=false;
  },true);
  document.addEventListener('keydown',function(ev){
    var nav=menu();
    if(ev.key==='Escape'&&nav&&nav.open){
      nav.open=false;
      nav.querySelector('summary').focus();
    }
  });
  window.addEventListener('resize',function(){
    var nav=menu();
    if(nav&&window.matchMedia('(min-width: 1024px)').matches)nav.open=false;
  });
  // The entry component signals its first committed render. Mutating the
  // navbar at DOMContentLoaded races React hydration on slower phones.
  document.addEventListener('nbc:hydrated',start,{once:true});
})();
"""

# The marker embeds a hash of the runtime, so editing the code above is
# enough to make the next patch run replace an older injected copy.
INLINER_MARK = (
    "/*nbc-runtime-" + hashlib.sha1(_RUNTIME.encode()).hexdigest()[:8] + "*/"
)
INLINER = INLINER_MARK + _RUNTIME


# Matches the collapsible-section state hook in both the server and client
# bundles (minified variable names differ between them):
#   [s,o]=X.useState(r); useEffect(()=>{n.state==="idle"&&o(r)},[n.state]);
#   let a=fn(e,i,t); return !i.children ...
PATTERN = re.compile(
    r'\[(\w),(\w)\]=([\w$]+(?:\.default)?)\.useState\((\w)\);'
    r'\(0,([\w$]+)\.useEffect\)\(\(\)=>\{(\w)\.state==="idle"&&\2\(\4\)\},'
    r'\[\6\.state\]\);let (\w)=[\w$]+\(([^)]*)\);return!(\w)\.c'
)


def patched(src):
    def repl(m):
        s, o, hook, active, eff, nav, let_var, fn_args, heading = m.groups()
        keep_open = f'({heading}.level===1||{active})'
        return (
            f'[{s},{o}]={hook}.useState({keep_open});'
            f'(0,{eff}.useEffect)(()=>{{{nav}.state==="idle"&&{o}({keep_open})}},'
            f'[{nav}.state]);let {let_var}='
            + m.group(0).split(f'let {let_var}=', 1)[1]
        )

    return PATTERN.subn(repl, src)


def patch_mobile_navigation():
    component = Path(HERE, "mobile_navigation.js").read_text()
    helpers = [
        {"NBC_JSX": "$p", "NBC_CONFIG": "py", "NBC_BASE": "pg", "NBC_URL": "Zm"},
        {"NBC_JSX": "Tt", "NBC_CONFIG": "_r", "NBC_BASE": "si", "NBC_URL": "$t"},
    ]
    button = re.compile(
        r'\(0,([\w$]+)\.jsxs\)\("button",\{className:"myst-top-nav-menu-button'
        r'.*?children:"Open Menu"\}\)\]\}\)'
    )
    for path, symbols in zip(TARGETS, helpers):
        src = Path(path).read_text()
        if "/*nbc-native-menu-start*/" not in src:
            src, count = button.subn(
                lambda m: f'(0,{m[1]}.jsx)(nbcMobileNavigation,{{}})', src
            )
            if count != 1:
                sys.exit(f"mobile navigation button not found in {path}; theme changed?")
        else:
            src = re.sub(
                r'/\*nbc-native-menu-start\*/.*?/\*nbc-native-menu-end\*/',
                '', src, flags=re.S,
            ).rstrip()
        rendered = re.sub(r'NBC_\w+', lambda m: symbols[m[0]], component)
        Path(path).write_text(
            src.rstrip() + '\n/*nbc-native-menu-start*/\n' + rendered
            + '/*nbc-native-menu-end*/\n'
        )
    print("patched native mobile navigation (server and client)")


def cache_bust_navigation():
    """Version the changed bundles AND their importers, including the manifest.

    Renaming just the entry leaves cached shared chunks in use. Keep canonical
    files so repeated patches can generate a fresh, consistent dependency graph.
    """
    pub = Path(THEME, "public", "build")
    sources = {
        p.name: (p, p.read_text()) for p in pub.rglob("*.js")
        if "-nbc-" not in p.name
    }
    changed = {"chunk-RUUCG5OS.js", "entry.client-NBCRT2.js"}
    version = hashlib.sha256(
        (INLINER + ''.join(sources[name][1] for name in sorted(changed))).encode()
    ).hexdigest()[:12]
    importers = {}
    for name, (_, src) in sources.items():
        for dependency in re.findall(r'[\w.$-]+\.js', src):
            importers.setdefault(dependency, set()).add(name)
    pending = list(changed)
    while pending:
        for name in importers.get(pending.pop(), set()) - changed:
            changed.add(name)
            pending.append(name)
    names = {name: name[:-3] + f"-nbc-{version}.js" for name in changed}
    pattern = re.compile(r'[\w.$-]+\.js')

    def rewrite(src):
        src = re.sub(r'-nbc-[0-9a-f]{12}(?=\.js)', '', src)
        return pattern.sub(lambda m: names.get(m[0], m[0]), src)

    for name in sorted(changed):
        path, src = sources[name]
        path.with_name(names[name]).write_text(rewrite(src))
    server = Path(THEME, "build", "index.js")
    server.write_text(rewrite(server.read_text()))
    print(f"versioned {len(changed)} navigation bundles and importers ({version})")


def main():
    if not os.path.isdir(THEME):
        sys.exit("book-theme template not found; run `myst build` first")
    total = 0
    # dev server: drop the 1-year immutable cache so patched bundles reload
    server_js = os.path.join(THEME, "server.js")
    if os.path.exists(server_js):
        with open(server_js) as f:
            ssrc = f.read()
        fixed = ssrc.replace(
            "{ immutable: true, maxAge: '1y' }", "{ maxAge: '5m' }"
        )
        if fixed != ssrc:
            with open(server_js, "w") as f:
                f.write(fixed)
            print("patched server.js (cache headers)")
    # inject the search runtime into the server-rendered HTML itself; the
    # document is never long-cached, unlike the fingerprinted JS bundles
    import json
    server_bundle = os.path.join(THEME, "build", "index.js")
    with open(server_bundle) as f:
        bsrc = f.read()
    tag = json.dumps("<script>" + INLINER + "</script></body>")
    if INLINER_MARK in bsrc:
        print("already patched: build/index.js (search runtime)")
    elif "nbc-runtime" in bsrc:  # older runtime: swap it out
        new_bsrc, n = re.subn(
            r'"<script>/\*nbc-runtime-[^*]+\*/(?:\\.|[^"\\])*</script></body>"',
            lambda m: tag,
            bsrc,
        )
        if n != 1:
            sys.exit("previous runtime injection not found; theme version changed?")
        with open(server_bundle, "w") as f:
            f.write(new_bsrc)
        total += n
        print(f"updated build/index.js runtime ({n} site)")
    else:
        new_bsrc, n = re.subn(
            r'new Response\("<!DOCTYPE html>"\+(\w+),',
            lambda m: (
                'new Response("<!DOCTYPE html>"+'
                f'{m.group(1)}.replace("</body>",{tag}),'
            ),
            bsrc,
        )
        if n == 0:
            sys.exit("SSR injection point not found; theme version changed?")
        with open(server_bundle, "w") as f:
            f.write(new_bsrc)
        total += n
        print(f"patched build/index.js (search runtime, {n} site)")
    # rename the patched entry + manifest so browsers that cached the stock
    # bundles (1-year immutable) fetch the patched versions
    rename = [("entry.client-PCJPW7TK", "entry.client-NBCRT2"),
              ("manifest-C732C875", "manifest-NBCRT2")]
    pub = os.path.join(THEME, "public", "build")
    if not os.path.exists(os.path.join(pub, "entry.client-NBCRT2.js")):
        import shutil
        for old, new in rename:
            shutil.copyfile(
                os.path.join(pub, f"{old}.js"), os.path.join(pub, f"{new}.js")
            )
        entry = os.path.join(pub, "entry.client-NBCRT2.js")
        with open(entry) as f:
            src = f.read()
        root = "children:(0,e.jsx)(r,{})"
        if src.count(root) != 1:
            sys.exit("client hydration entry not found; theme version changed?")
        src = src.replace(root, "children:(0,e.jsx)(nbcReady,{})")
        src += (
            '\nfunction nbcReady(){t.useEffect(()=>{'
            'document.dispatchEvent(new Event("nbc:hydrated"))},[]);'
            'return (0,e.jsx)(r,{})}\n'
        )
        with open(entry, "w") as f:
            f.write(src)
        for path in [os.path.join(THEME, "build", "index.js")] + [
            os.path.join(pub, "manifest-NBCRT2.js")
        ]:
            with open(path) as f:
                s = f.read()
            for old, new in rename:
                s = s.replace(old, new)
            s = s.replace("entry.client-NBCRT1", "entry.client-NBCRT2")
            s = s.replace("manifest-NBCRT1", "manifest-NBCRT2")
            with open(path, "w") as f:
                f.write(s)
        print("renamed entry.client + manifest (cache bust)")

    # Hydration can start as soon as the scripts arrive; navigation does not
    # depend on it, and search need not wait for an idle browser either.
    entry = Path(pub, "entry.client-NBCRT2.js")
    entry.write_text(entry.read_text().replace(
        "window.requestIdleCallback?window.requestIdleCallback(d):window.setTimeout(d,1);",
        "d();",
    ))

    for path in TARGETS:
        with open(path) as f:
            src = f.read()
        if ".level===1||" in src:
            print(f"already patched: {os.path.relpath(path, THEME)}")
            continue
        out, n = patched(src)
        if n == 0:
            sys.exit(f"pattern not found in {path}; theme version changed?")
        with open(path, "w") as f:
            f.write(out)
        total += n
        print(f"patched {os.path.relpath(path, THEME)} ({n} site)")
    patch_mobile_navigation()
    cache_bust_navigation()
    print(f"done ({total} replacements)")


if __name__ == "__main__":
    main()
