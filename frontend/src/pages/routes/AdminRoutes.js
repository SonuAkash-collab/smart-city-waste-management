import { get, post } from '../../api.js';
import RouteMap from '../../components/RouteMap.js';
import { Badge, html, Notice, todayIso, useEffect, useState, wasteLabel } from '../../lib.js';

function StopList({ route }) {
  return html`
    <table class="responsive">
      <thead><tr><th>#</th><th>Stop</th><th>Load after (kg)</th><th>Status</th></tr></thead>
      <tbody>
        ${route.stops.map(
          (s) => html`<tr key=${s.id}>
            <td data-label="#">${s.sequence}</td>
            <td data-label="Stop">
              ${s.stopType === 'FACILITY'
                ? html`<strong>Unload</strong> at ${s.facilityName}`
                : html`Request #${s.requestId} · ${wasteLabel(s.wasteType)} ${s.quantityKg} kg<br /><span class="hint">${s.address || ''}</span>`}
            </td>
            <td data-label="Load after">${s.loadAfterKg} / ${route.vehicleCapacityKg}</td>
            <td data-label="Status"><${Badge} kind=${s.status}>${s.status}<//></td>
          </tr>`,
        )}
      </tbody>
    </table>
  `;
}

export default function AdminRoutes() {
  const [day, setDay] = useState(todayIso());
  const [routes, setRoutes] = useState([]);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const load = async () => {
    try {
      setRoutes(await get('/routes', { date: day }));
    } catch (err) {
      setError(err.message);
    }
  };
  useEffect(() => {
    setResult(null);
    load();
  }, [day]);

  const generateRoutes = async () => {
    setBusy(true);
    setError('');
    try {
      const outcome = await post('/routes/generate', { date: day });
      setResult(outcome);
      setRoutes(outcome.routes);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return html`
    <div class="page-head">
      <div><h1>Collection routes</h1><p class="muted">Plan routes from approved requests: priority first, then nearest stop.</p></div>
    </div>
    <section class="card row">
      <div><label for="r-day">Route date</label><input id="r-day" type="date" value=${day} onChange=${(e) => setDay(e.target.value)} /></div>
      <div style=${{ flex: '0 0 auto' }}><button onClick=${generateRoutes} disabled=${busy}>${busy ? 'Planning…' : 'Generate routes'}</button></div>
    </section>
    <${Notice} kind="error">${error}<//>
    ${result && html`<${Notice} kind="success">${result.message}<//>`}
    ${result && result.alerts.map((a, i) => html`<${Notice} key=${'a' + i} kind="warn">${a.message}<//>`)}
    ${result && result.unassigned.length > 0 &&
    html`<${Notice} kind="warn">Not planned: ${result.unassigned.map((u) => `#${u.requestId} (${u.reason.replace(/_/g, ' ').toLowerCase()})`).join(', ')}. They stay approved for the next run.<//>`}
    ${routes.length > 0
      ? html`<section class="card"><${RouteMap} routes=${routes} tall=${true} /></section>
          ${routes.map(
            (route) => html`<section class="card" key=${route.id}>
              <div class="page-head" style=${{ marginBottom: '0.5rem' }}>
                <div>
                  <h2>Route ${route.id} · ${route.vehicleRegistration}</h2>
                  <p class="muted">Driver: ${route.driverName || 'none'} · ${route.totalDistanceKm} km · ${route.stops.length} stops</p>
                </div>
                <${Badge} kind=${route.status}>${route.status}<//>
              </div>
              <${StopList} route=${route} />
            </section>`,
          )}`
      : html`<section class="card"><p class="muted">No routes for this date yet.</p></section>`}
  `;
}
