import { get } from '../../api.js';
import { baseMap } from '../../components/MapPicker.js';
import { Badge, formatDateTime, html, L, Notice, useEffect, useRef, useState, wasteLabel } from '../../lib.js';

const STEPS = ['SUBMITTED', 'APPROVED', 'SCHEDULED', 'COLLECTED'];

export default function RequestDetail({ params }) {
  const [item, setItem] = useState(null);
  const [error, setError] = useState('');
  const holder = useRef(null);

  useEffect(() => {
    get(`/requests/${params.id}`).then(setItem).catch((err) => setError(err.message));
  }, [params.id]);

  useEffect(() => {
    if (!item || !holder.current) return undefined;
    const map = baseMap(holder.current, [item.latitude, item.longitude], 16);
    L.marker([item.latitude, item.longitude]).addTo(map);
    return () => map.remove();
  }, [item]);

  if (error) return html`<${Notice} kind="error">${error}<//>`;
  if (!item) return html`<p class="muted">Loading…</p>`;
  const reached = STEPS.indexOf(item.status);
  return html`
    <div class="page-head">
      <div><h1>Request #${item.id}</h1><p class="muted">${wasteLabel(item.wasteType)} · ${item.estimatedQuantityKg} kg · sent ${formatDateTime(item.createdAt)}</p></div>
      <${Badge} kind=${item.status}>${item.status}<//>
    </div>
    <section class="card">
      <ol class="timeline">
        ${STEPS.map((s, i) => html`<li key=${s} class=${i <= reached ? 'done' : ''}>${s.toLowerCase()}</li>`)}
      </ol>
      ${['REJECTED', 'MISSED', 'CANCELLED'].includes(item.status) &&
      html`<${Notice} kind="warn">This request was ${item.status.toLowerCase()}${item.reason ? `: ${item.reason}` : '.'}<//>`}
      ${item.scheduledDate && html`<p>Planned for collection on <strong>${item.scheduledDate}</strong>.</p>`}
      <p>Priority <${Badge} kind=${item.priority}>${item.priority}<//>${item.priorityOverridden ? ' (set by the city)' : ''}</p>
      <p class="muted">${item.address || ''}</p>
    </section>
    <section class="card"><div ref=${holder} class="map"></div></section>
    ${item.photo && html`<section class="card"><img alt="Photo of the waste" style=${{ maxWidth: '100%', borderRadius: '8px' }} src=${`data:image/*;base64,${item.photo}`} /></section>`}
    <p><a href="#/requests/mine">← Back to my requests</a></p>
  `;
}
