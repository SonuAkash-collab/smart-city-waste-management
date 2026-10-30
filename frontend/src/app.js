import { html, ReactDOM, useEffect, useState } from './lib.js';
import Login from './pages/auth/Login.js';
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

// Each role only sees its own menu items (SCW-F-002). The server still checks
// every call, so hiding a link is never the only protection.
export function canOpen(page, user) {
  if (page.guestOnly) return !user;
  if (!page.roles) return true;
  return Boolean(user) && page.roles.includes(user.role);
}

function menuItems(user) {
  return pages.filter((page) => page.menu !== false && canOpen(page, user));
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
      ${menuItems(user).map(
        (item) =>
          html`<a key=${item.path} href=${'#' + item.path} class=${path === item.path ? 'active' : ''}
            >${item.label}</a
          >`,
      )}
    </nav>
  `;
}

function Forbidden() {
  return html`<section class="card"><h2>Not available for your role</h2>
    <p class="muted">This page belongs to another type of account.</p><p><a href="#/">Go home</a></p></section>`;
}

function NotFound() {
  return html`<section class="card"><h2>Page not found</h2><p><a href="#/">Go home</a></p></section>`;
}

function App() {
  const { path, user } = useRoute();
  const found = findPage(path);
  let Page = found ? found.page.component : NotFound;
  if (found && found.page.roles && !user) Page = Login;
  else if (found && found.page.guestOnly && user) Page = pages[0].component;
  else if (found && !canOpen(found.page, user)) Page = Forbidden;
  return html`
    <${Header} user=${user} path=${path} />
    <main class="content">
      <${Page} key=${path} params=${found ? found.params : {}} user=${user} />
    </main>
    <footer class="footer">Team 04 · Smart City Waste Management System</footer>
  `;
}

ReactDOM.createRoot(document.getElementById('root')).render(html`<${App} />`);
