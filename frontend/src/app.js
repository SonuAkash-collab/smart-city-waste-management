import { get } from './api.js';
import Icon from './components/Icon.js';
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

function initials(name) {
  return (name || '?')
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join('');
}

function Brand() {
  return html`<a class="rail-brand" href="#/">
    <span class="mark"><${Icon} name="bin" /></span>
    <span class="wordmark">Smart City Waste<small>Collection & routing</small></span>
  </a>`;
}

// Unread notifications for the menu badge, refreshed on every page change.
function useUnread(user, path) {
  const [unread, setUnread] = useState(0);
  useEffect(() => {
    if (!user) return;
    get('/notifications')
      .then((data) => setUnread(data.unread || 0))
      .catch(() => setUnread(0));
  }, [user, path]);
  return unread;
}

// Menu items grouped by their `group` field, in the order of pages/index.js.
function groupItems(items) {
  const groups = [];
  items.forEach((item) => {
    const name = item.group || 'Menu';
    let group = groups.find((g) => g.name === name);
    if (!group) {
      group = { name, items: [] };
      groups.push(group);
    }
    group.items.push(item);
  });
  return groups;
}

function Sidebar({ user, path }) {
  const unread = useUnread(user, path);
  const logout = () => {
    clearSession();
    navigate('/login');
  };
  return html`
    <aside class="rail">
      <${Brand} />
      <nav aria-label="Main menu">
        ${groupItems(menuItems(user)).map(
          (group) => html`<div key=${group.name}>
            <div class="nav-group">${group.name}</div>
            ${group.items.map(
              (item) => html`<a key=${item.path} href=${'#' + item.path}
                class=${'nav-link' + (path === item.path ? ' active' : '')}
                aria-current=${path === item.path ? 'page' : undefined}>
                <${Icon} name=${item.icon} />
                <span>${item.label}</span>
                ${item.path === '/notifications' && unread > 0 && html`<span class="nav-count">${unread}</span>`}
              </a>`,
            )}
          </div>`,
        )}
      </nav>
      <div class="rail-user">
        <span class="avatar" aria-hidden="true">${initials(user.fullName)}</span>
        <span class="who"><strong>${user.fullName}</strong><span class="role">${user.role.toLowerCase()}</span></span>
        <button class="icon-btn" title="Log out" aria-label="Log out" onClick=${logout}><${Icon} name="logout" /></button>
      </div>
    </aside>
  `;
}

function GuestTop() {
  return html`<header class="guest-top">
    <${Brand} />
    <nav aria-label="Account">
      <a href="#/login">Log in</a>
      <a class="cta" href="#/register">Create account</a>
    </nav>
  </header>`;
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
  const page = html`<${Page} key=${path} params=${found ? found.params : {}} user=${user} />`;
  const footer = html`<footer class="footer">Team 04 · Smart City Waste Management System</footer>`;

  if (!user) {
    return html`<div class="guest">
      <${GuestTop} />
      <main class="content">${page}</main>
      ${footer}
    </div>`;
  }
  return html`<div class="shell">
    <${Sidebar} user=${user} path=${path} />
    <div class="main-area">
      <main class="content">${page}</main>
      ${footer}
    </div>
  </div>`;
}

ReactDOM.createRoot(document.getElementById('root')).render(html`<${App} />`);
