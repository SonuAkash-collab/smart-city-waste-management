import { get, patch } from '../../api.js';
import RouteMap from '../../components/RouteMap.js';
import { Badge, html, Notice, useEffect, useState, wasteLabel } from '../../lib.js';

function StopCard({ route, stop, onDone }) {
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
  return html`
    <div class="card stack" style=${{ marginBottom: '0.75rem' }}>
      <div class="page-head" style=${{ marginBottom: 0 }}>
        <h3>${stop.sequence}. ${facility ? `Unload at ${stop.facilityName}` : `Pick up request #${stop.requestId}`}</h3>
        <${Badge} kind=${stop.status}>${stop.status}<//>
      </div>
      ${facility
        ? html`<p class="muted">Empty the vehicle here before the next pickups.</p>`
        : html`<p>${wasteLabel(stop.wasteType)} · about ${stop.quantityKg} kg<br /><span class="muted">${stop.address || `${stop.latitude.toFixed(5)}, ${stop.longitude.toFixed(5)}`}</span></p>`}
      ${stop.status === 'PENDING' &&
      html`<div class="actions">
        <button disabled=${busy} onClick=${() => mark('COLLECTED')}>${facility ? 'Unloaded' : 'Collected'}</button>
        ${!facility && html`<button class="ghost" disabled=${busy} onClick=${() => mark('MISSED')}>Missed</button>`}
        <a class="button ghost" target="_blank" rel="noopener"
          href=${`https://www.openstreetmap.org/directions?to=${stop.latitude},${stop.longitude}`}>Directions</a>
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
    return html`<section class="card"><h1>My route</h1><p class="muted">No route is assigned to you right now.</p></section>`;
  }
  const route = routes[0];
  const left = route.stops.filter((s) => s.status === 'PENDING').length;
  return html`
    <div class="page-head">
      <div>
        <h1>My route · ${route.date}</h1>
        <p class="muted">${route.vehicleRegistration} · ${route.totalDistanceKm} km · ${left} of ${route.stops.length} stops left</p>
      </div>
      <${Badge} kind=${route.status}>${route.status}<//>
    </div>
    <section class="card"><${RouteMap} routes=${[route]} /></section>
    ${route.stops.map((stop) => html`<${StopCard} key=${stop.id} route=${route} stop=${stop} onDone=${load} />`)}
  `;
}
