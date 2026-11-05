import { get, patch } from '../../api.js';
import Icon from '../../components/Icon.js';
import RouteMap from '../../components/RouteMap.js';
import { Badge, html, Notice, useEffect, useState, wasteLabel } from '../../lib.js';

function StopCard({ route, stop, onDone, next }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const mark = async (status) => {
    setBusy(true);
    setError('');
    try {
      await patch(`/routes/${route.id}/stops/${stop.id}`, { status });
      onDone();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };
  const facility = stop.stopType === 'FACILITY';
  const done = stop.status !== 'PENDING';
  return html`
    <div class=${'card stop-card' + (next ? ' next' : '') + (done ? ' done' : '')}>
      ${next && html`<span class="next-tag">Next stop</span>`}
      <div class="stop-head">
        <span class=${'seq' + (facility ? ' f' : '')}>${facility ? 'F' : stop.sequence}</span>
        <h3>${facility ? `Unload at ${stop.facilityName}` : `Pick up request #${stop.requestId}`}</h3>
        <${Badge} kind=${stop.status}>${stop.status}<//>
      </div>
      ${facility
        ? html`<p class="muted">Empty the vehicle here before the next pickups.</p>`
        : html`<p>${wasteLabel(stop.wasteType)} · about ${stop.quantityKg} kg<br /><span class="muted">${stop.address || `${stop.latitude.toFixed(5)}, ${stop.longitude.toFixed(5)}`}</span></p>`}
      ${stop.status === 'PENDING' &&
      html`<div class="stop-actions">
        <button class="big" disabled=${busy} onClick=${() => mark('COLLECTED')}><${Icon} name="check" /> ${facility ? 'Unloaded' : 'Collected'}</button>
        ${!facility && html`<button class="big danger" disabled=${busy} onClick=${() => mark('MISSED')}><${Icon} name="x" /> Missed</button>`}
        <a class="button ghost big" target="_blank" rel="noopener"
          href=${`https://www.openstreetmap.org/directions?to=${stop.latitude},${stop.longitude}`}><${Icon} name="navigation" /> Directions</a>
      </div>`}
      ${error && html`<p class="hint" style=${{ color: 'var(--red)' }}>${error}</p>`}
    </div>
  `;
}

export default function DriverRoute() {
  const [routes, setRoutes] = useState(null);
  const [error, setError] = useState('');

  const load = async () => {
    try {
      setRoutes(await get('/routes/assigned'));
    } catch (err) {
      setError(err.message);
    }
  };
  useEffect(() => {
    load();
  }, []);

  if (error) return html`<${Notice} kind="error">${error}<//>`;
  if (!routes) return html`<p class="muted">Loading your route…</p>`;
  if (!routes.length) {
    return html`<section class="card empty">
      <span class="how-icon"><${Icon} name="navigation" /></span>
      <h2>My route</h2>
      <p class="muted">No route is assigned to you right now. You will get a notification when one is.</p>
    </section>`;
  }
  const route = routes[0];
  const left = route.stops.filter((s) => s.status === 'PENDING').length;
  const doneCount = route.stops.length - left;
  const next = route.stops.find((s) => s.status === 'PENDING');
  return html`
    <div class="page-head">
      <div>
        <span class="eyebrow">Today · ${route.date}</span>
        <h1>My route</h1>
        <p class="muted">${route.vehicleRegistration} · ${route.totalDistanceKm} km</p>
      </div>
      <${Badge} kind=${route.status}>${route.status}<//>
    </div>
    <section class="card route-progress">
      <div class="rp-count"><strong>${doneCount}</strong> of ${route.stops.length} stops done</div>
      <div class="bar lg"><span style=${{ width: `${(100 * doneCount) / route.stops.length}%` }}></span></div>
      ${left === 0 && html`<p class="muted" style=${{ marginTop: '0.6rem' }}>All stops are done. Good work!</p>`}
    </section>
    <section class="card"><${RouteMap} routes=${[route]} /></section>
    ${route.stops.map((stop) => html`<${StopCard} key=${stop.id} route=${route} stop=${stop} onDone=${load} next=${next && next.id === stop.id} />`)}
  `;
}
