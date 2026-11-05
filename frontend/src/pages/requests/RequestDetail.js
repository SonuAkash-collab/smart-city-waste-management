import { get } from '../../api.js';
import Icon from '../../components/Icon.js';
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
  const stopped = ['REJECTED', 'MISSED', 'CANCELLED'].includes(item.status);
  return html`
    <div class="page-head">
      <div>
        <span class="eyebrow">Pickup request</span>
        <h1>Request #${item.id}</h1>
        <p class="muted">${wasteLabel(item.wasteType)} · ${item.estimatedQuantityKg} kg · sent ${formatDateTime(item.createdAt)}</p>
      </div>
      <${Badge} kind=${item.status}>${item.status}<//>
    </div>
    <div class="split">
      <section class="card">
        <h2>Progress</h2>
        <ol class="timeline">
          ${STEPS.map((s, i) => html`<li key=${s} class=${i < reached || (i === reached && s === 'COLLECTED') ? 'done' : i === reached ? 'done current' : ''}>${s.toLowerCase()}</li>`)}
        </ol>
        ${stopped && html`<${Notice} kind="warn">This request was ${item.status.toLowerCase()}${item.reason ? `: ${item.reason}` : '.'}<//>`}
        <dl class="detail-list">
          <dt>Waste</dt><dd>${wasteLabel(item.wasteType)}</dd>
          <dt>Quantity</dt><dd>${item.estimatedQuantityKg} kg</dd>
          <dt>Priority</dt><dd><${Badge} kind=${item.priority}>${item.priority}<//>${item.priorityOverridden ? html` <span class="hint">set by the city</span>` : ''}</dd>
          <dt>Collection</dt><dd>${item.scheduledDate ? html`Planned for <strong>${item.scheduledDate}</strong>` : html`<span class="hint">Not planned yet</span>`}</dd>
          ${item.address && html`<dt>Address</dt><dd>${item.address}</dd>`}
        </dl>
        ${item.photo && html`<img alt="Photo of the waste" style=${{ maxWidth: '100%', borderRadius: '8px', marginTop: '1rem' }} src=${`data:image/*;base64,${item.photo}`} />`}
      </section>
      <section class="card"><div ref=${holder} class="map tall"></div></section>
    </div>
    <p><a class="back" href="#/requests/mine"><${Icon} name="arrow" /> Back to my requests</a></p>
  `;
}
