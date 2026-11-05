import { get, patch, post } from '../api.js';
import { formatDateTime, html, Notice, useEffect, useState } from '../lib.js';

export default function Notifications() {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const load = () => get('/notifications').then(setData).catch((err) => setError(err.message));
  useEffect(() => {
    load();
  }, []);

  const read = (n) => !n.isRead && patch(`/notifications/${n.id}/read`).then(load);
  const readAll = () => post('/notifications/read-all').then(load);

  return html`
    <div class="page-head">
      <div><h1>Notifications</h1><p class="muted">${data ? `${data.unread} unread` : ''}</p></div>
      ${data && data.unread > 0 && html`<button class="ghost" onClick=${readAll}>Mark all read</button>`}
    </div>
    <${Notice} kind="error">${error}<//>
    <section class="card">
      ${!data
        ? html`<p class="muted">Loading…</p>`
        : data.items.length === 0
          ? html`<p class="muted">Nothing yet. You will see every status change here.</p>`
          : data.items.map((n) => html`<div key=${n.id} onClick=${() => read(n)}
              style=${{ padding: '0.7rem 0', borderBottom: '1px solid var(--line)', cursor: n.isRead ? 'default' : 'pointer', fontWeight: n.isRead ? 400 : 600 }}>
              ${n.message}<br /><span class="hint">${formatDateTime(n.createdAt)}${n.isRead ? '' : ' · tap to mark read'}</span>
            </div>`)}
    </section>
  `;
}
