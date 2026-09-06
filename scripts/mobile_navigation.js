// Rendered identically by the server and client. The browser owns disclosure
// state, so taps work before hydration, during hydration, and without scripts.
// The patcher substitutes the theme's JSX, config, and URL helper identifiers.
function nbcMobileNavigation() {
  const config = NBC_CONFIG() || {};
  const base = NBC_BASE();
  function items(nav) {
    return (nav || []).map((item, index) => NBC_JSX.jsx('li', {
      children: item.children ? NBC_JSX.jsxs('details', {
        className: 'nbc-mobile-group',
        suppressHydrationWarning: true,
        children: [
          NBC_JSX.jsx('summary', {children: item.title}),
          NBC_JSX.jsx('ul', {children: items(item.children)})
        ]
      }) : NBC_JSX.jsx('a', {
        href: NBC_URL(item.url, base),
        children: item.title
      })
    }, item.url || item.title || index));
  }
  return NBC_JSX.jsxs('details', {
    className: 'nbc-mobile-menu',
    suppressHydrationWarning: true,
    children: [
      NBC_JSX.jsxs('summary', {
        className: 'nbc-mobile-menu-toggle',
        'aria-label': 'Navigation menu',
        children: [
          NBC_JSX.jsx('span', {'aria-hidden': true, children: '☰'}),
          NBC_JSX.jsx('span', {className: 'sr-only', children: 'Menu'})
        ]
      }),
      NBC_JSX.jsx('div', {
        className: 'nbc-mobile-menu-panel',
        children: NBC_JSX.jsx('ul', {
          children: items([{title: 'Home', url: '/'}, ...(config.nav || [])])
        })
      })
    ]
  });
}
