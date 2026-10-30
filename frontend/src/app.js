import { html, ReactDOM, useEffect, useState } from './lib.js';
import { findPage, pages } from './pages/index.js';
import { clearSession, getUser } from './session.js';

function currentPath() {
  const hash = window.location.hash.replace(/^#/, '');
  return hash.split('?')[0] || '/';
}

export function navigate(path) {
  window.location.hash = path;
}

function useRoute() {
  const [path, setPath] = useState(currentPath());
  const [user, setUser] = useState(getUser());
  useEffect(() => {
    const onHash = () => setPath(currentPath());
    const onSession = () => setUser(getUser());
    window.addEventListener('hashchange', onHash);
    window.addEventListener('session-changed', onSession);
    return () => {
      window.removeEventListener('hashchange', onHash);
      window.removeEventListener('session-changed', onSession);
    };
  }, []);
  return { path, user };
}

function menuItems() {
  return pages.filter((page) => page.menu !== false);
}

function Header({ user, path }) {
  const logout = () => {
    clearSession();
    navigate('/login');
  };
  return html`
    <header class="topbar">
      <a class="brand" href="#/">
        <span class="logo" aria-hidden="true"></span>
        <span>Smart City Waste</span>
      </a>
      ${user &&
      html`<div class="who">
        <span class="who-name">${user.fullName}</span>
        <span class="who-role">${user.role}</span>
        <button class="ghost small" onClick=${logout}>Log out</button>
      </div>`}
    </header>
    <nav class="menu" aria-label="Main menu">
      ${menuItems().map(
        (item) =>
          html`<a key=${item.path} href=${'#' + item.path} class=${path === item.path ? 'active' : ''}
            >${item.label}</a
          >`,
      )}
    </nav>
  `;
}

function NotFound() {
  return html`<section class="card"><h2>Page not found</h2><p><a href="#/">Go home</a></p></section>`;
}

function App() {
  const { path, user } = useRoute();
  const found = findPage(path);
  const Page = found ? found.page.component : NotFound;
  return html`
    <${Header} user=${user} path=${path} />
    <main class="content">
      <${Page} key=${path} params=${found ? found.params : {}} user=${user} />
    </main>
    <footer class="footer">Team 04 · Smart City Waste Management System</footer>
  `;
}

ReactDOM.createRoot(document.getElementById('root')).render(html`<${App} />`);
