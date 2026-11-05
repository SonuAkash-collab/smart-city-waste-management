import { del, get } from '../../api.js';
import Icon from '../../components/Icon.js';
import { Badge, formatDateTime, html, Notice, useEffect, useState, wasteLabel } from '../../lib.js';

const CANCELLABLE = ['SUBMITTED', 'APPROVED'];

export default function MyRequests() {
  const [data, setData] = useState(null);
  const [message, setMessage] = useState({ kind: 'info', text: '' });
  const [page, setPage] = useState(1);

  const load = async () => {
    try {
      setData(await get('/requests', { page, size: 10 }));
    } catch (err) {
      setMessage({ kind: 'error', text: err.message });
    }
  };
  useEffect(() => {
    load();
  }, [page]);

  const cancel = async (item) => {
    if (!window.confirm(`Cancel request #${item.id}?`)) return;
    try {
      await del(`/requests/${item.id}`);
      setMessage({ kind: 'success', text: `Request #${item.id} was cancelled.` });
      load();
    } catch (err) {
      setMessage({ kind: 'error', text: err.message });
    }
  };

  const pages = data ? Math.max(1, Math.ceil(data.total / 10)) : 1;
  return html`
    <div class="page-head">
      <div>
        <span class="eyebrow">Pickups</span>
        <h1>My requests</h1>
        <p class="muted">Follow each pickup from approval to collection.${data ? ` ${data.total} in total.` : ''}</p>
      </div>
      <a class="button" href="#/requests/new"><${Icon} name="plus" /> New request</a>
    </div>
    <${Notice} kind=${message.kind}>${message.text}<//>
    <section class="card">
      ${!data
        ? html`<p class="muted">Loading…</p>`
        : data.items.length === 0
          ? html`<div class="empty">
              <span class="how-icon"><${Icon} name="inbox" /></span>
              <h3>No pickups yet</h3>
              <p class="muted">Request your first pickup. It takes under a minute.</p>
              <a class="button" href="#/requests/new">Request a pickup</a>
            </div>`
          : html`<table class="responsive">
              <thead><tr><th>Request</th><th>Waste</th><th>Priority</th><th>Status</th><th></th></tr></thead>
              <tbody>
                ${data.items.map(
                  (item) => html`<tr key=${item.id}>
                    <td data-label="Request"><a href=${`#/requests/${item.id}`}><strong>#${item.id}</strong></a><br /><span class="hint">${formatDateTime(item.createdAt)}</span></td>
                    <td data-label="Waste">${wasteLabel(item.wasteType)} · ${item.estimatedQuantityKg} kg</td>
                    <td data-label="Priority"><${Badge} kind=${item.priority}>${item.priority}<//></td>
                    <td data-label="Status"><${Badge} kind=${item.status}>${item.status}<//></td>
                    <td data-label="">
                      <div class="actions">
                        <a class="button ghost small" href=${`#/requests/${item.id}`}>Details</a>
                        ${CANCELLABLE.includes(item.status) &&
                        html`<button class="small danger" onClick=${() => cancel(item)}>Cancel</button>`}
                      </div>
                    </td>
                  </tr>`,
                )}
              </tbody>
            </table>
            <div class="pager">
              <span class="hint">page ${page} of ${pages}</span>
              <button class="ghost small" disabled=${page <= 1} onClick=${() => setPage(page - 1)}>Previous</button>
              <button class="ghost small" disabled=${page >= pages} onClick=${() => setPage(page + 1)}>Next</button>
            </div>`}
    </section>
  `;
}
