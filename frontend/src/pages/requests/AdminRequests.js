import { get, patch } from '../../api.js';
import {
  Badge,
  formatDateTime,
  html,
  Notice,
  PRIORITIES,
  STATUSES,
  useEffect,
  useState,
  WASTE_TYPES,
  wasteLabel,
} from '../../lib.js';

const PAGE_SIZE = 10;

function DecisionRow({ item, onDone }) {
  const [priority, setPriority] = useState('');
  const [reason, setReason] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const open = item.status === 'SUBMITTED' || item.status === 'APPROVED';

  const decide = async (status) => {
    setBusy(true);
    setError('');
    try {
      await patch(`/requests/${item.id}/status`, {
        status,
        priority: priority || null,
        reason: reason || null,
      });
      onDone();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return html`
    <tr>
      <td data-label="Request"><strong>#${item.id}</strong><br /><span class="hint">${formatDateTime(item.createdAt)}</span></td>
      <td data-label="Waste">${wasteLabel(item.wasteType)} · ${item.estimatedQuantityKg} kg</td>
      <td data-label="Where">${item.address || `${item.latitude.toFixed(4)}, ${item.longitude.toFixed(4)}`}</td>
      <td data-label="Priority">
        <${Badge} kind=${item.priority}>${item.priority}<//>
        ${item.priorityOverridden && html`<span class="hint"> set by admin</span>`}
      </td>
      <td data-label="Status"><${Badge} kind=${item.status}>${item.status}<//></td>
      <td data-label="Decide">
        ${open
          ? html`<div class="stack" style=${{ minWidth: '200px' }}>
              <select value=${priority} onChange=${(e) => setPriority(e.target.value)} aria-label="Priority override">
                <option value="">Keep priority</option>
                ${PRIORITIES.map((p) => html`<option key=${p} value=${p}>${p}</option>`)}
              </select>
              <input value=${reason} onInput=${(e) => setReason(e.target.value)} placeholder="Reason (optional)" />
              <div class="actions">
                <button class="small" disabled=${busy} onClick=${() => decide('APPROVED')}>
                  ${item.status === 'APPROVED' ? 'Save' : 'Approve'}
                </button>
                <button class="small danger" disabled=${busy} onClick=${() => decide('REJECTED')}>Reject</button>
              </div>
              ${error && html`<span class="hint" style=${{ color: 'var(--red)' }}>${error}</span>`}
            </div>`
          : html`<span class="hint">${item.reason || '—'}</span>`}
      </td>
    </tr>
  `;
}

export default function AdminRequests() {
  const [filters, setFilters] = useState({ status: 'SUBMITTED', priority: '', wasteType: '', date: '' });
  const [page, setPage] = useState(1);
  const [data, setData] = useState(null);
  const [error, setError] = useState('');

  const load = async () => {
    setError('');
    try {
      setData(await get('/requests', { ...filters, page, size: PAGE_SIZE }));
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    load();
  }, [filters, page]);

  const setFilter = (key) => (e) => {
    setPage(1);
    setFilters({ ...filters, [key]: e.target.value });
  };
  const pages = data ? Math.max(1, Math.ceil(data.total / PAGE_SIZE)) : 1;

  return html`
    <div class="page-head">
      <div><h1>Collection requests</h1><p class="muted">Approve, reject or re-prioritise citizen requests.</p></div>
    </div>
    <section class="card">
      <div class="row">
        <div>
          <label for="f-status">Status</label>
          <select id="f-status" value=${filters.status} onChange=${setFilter('status')}>
            <option value="">All</option>
            ${STATUSES.map((s) => html`<option key=${s} value=${s}>${s}</option>`)}
          </select>
        </div>
        <div>
          <label for="f-priority">Priority</label>
          <select id="f-priority" value=${filters.priority} onChange=${setFilter('priority')}>
            <option value="">All</option>
            ${PRIORITIES.map((p) => html`<option key=${p} value=${p}>${p}</option>`)}
          </select>
        </div>
        <div>
          <label for="f-waste">Waste type</label>
          <select id="f-waste" value=${filters.wasteType} onChange=${setFilter('wasteType')}>
            <option value="">All</option>
            ${WASTE_TYPES.map((w) => html`<option key=${w.value} value=${w.value}>${w.label}</option>`)}
          </select>
        </div>
        <div>
          <label for="f-date">Submitted on</label>
          <input id="f-date" type="date" value=${filters.date} onChange=${setFilter('date')} />
        </div>
      </div>
    </section>
    <${Notice} kind="error">${error}<//>
    <section class="card">
      ${!data
        ? html`<p class="muted">Loading…</p>`
        : data.items.length === 0
          ? html`<p class="muted">No requests match these filters.</p>`
          : html`<table class="responsive">
              <thead><tr><th>Request</th><th>Waste</th><th>Where</th><th>Priority</th><th>Status</th><th>Decision</th></tr></thead>
              <tbody>${data.items.map((item) => html`<${DecisionRow} key=${item.id} item=${item} onDone=${load} />`)}</tbody>
            </table>
            <div class="pager">
              <span class="hint">${data.total} total · page ${page} of ${pages}</span>
              <button class="ghost small" disabled=${page <= 1} onClick=${() => setPage(page - 1)}>Previous</button>
              <button class="ghost small" disabled=${page >= pages} onClick=${() => setPage(page + 1)}>Next</button>
            </div>`}
    </section>
  `;
}
