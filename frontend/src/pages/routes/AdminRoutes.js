import { get, post } from '../../api.js';
import Icon from '../../components/Icon.js';
import RouteMap, { COLORS } from '../../components/RouteMap.js';
import { Badge, html, Notice, todayIso, useEffect, useState, wasteLabel } from '../../lib.js';

function StopList({ route }) {
  return html`
    <table class="responsive">
      <thead><tr><th>#</th><th>Stop</th><th>Load after (kg)</th><th>Status</th></tr></thead>
      <tbody>
        ${route.stops.map(
          (s) => html`<tr key=${s.id}>
            <td data-label="#"><span class=${'seq' + (s.stopType === 'FACILITY' ? ' f' : '')}>${s.stopType === 'FACILITY' ? 'F' : s.sequence}</span></td>
            <td data-label="Stop">
              ${s.stopType === 'FACILITY'
                ? html`<strong>Unload</strong> at ${s.facilityName}`
                : html`Request #${s.requestId} · ${wasteLabel(s.wasteType)} ${s.quantityKg} kg<br /><span class="hint">${s.address || ''}</span>`}
            </td>
            <td data-label="Load after">
              <span class="num">${s.loadAfterKg} / ${route.vehicleCapacityKg}</span>
              <div class="bar" style=${{ marginTop: '0.3rem' }}><span style=${{ width: `${Math.min(100, (100 * s.loadAfterKg) / route.vehicleCapacityKg)}%` }}></span></div>
            </td>
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

  const stops = routes.reduce((n, r) => n + r.stops.filter((s) => s.stopType !== 'FACILITY').length, 0);
  const km = routes.reduce((n, r) => n + r.totalDistanceKm, 0);
  return html`
    <div class="page-head">
      <div>
        <span class="eyebrow">Operations</span>
        <h1>Collection routes</h1>
        <p class="muted">Plan routes from approved requests: priority first, then nearest stop.</p>
      </div>
    </div>
    <section class="card toolbar">
      <div><label for="r-day">Route date</label><input id="r-day" type="date" value=${day} onChange=${(e) => setDay(e.target.value)} /></div>
      <button onClick=${generateRoutes} disabled=${busy}><${Icon} name="route" /> ${busy ? 'Planning…' : 'Generate routes'}</button>
    </section>
    <${Notice} kind="error">${error}<//>
    ${result && html`<${Notice} kind="success">${result.message}<//>`}
    ${result && result.alerts.map((a, i) => html`<${Notice} key=${'a' + i} kind="warn">${a.message}<//>`)}
    ${result && result.unassigned.length > 0 &&
    html`<${Notice} kind="warn">Not planned: ${result.unassigned.map((u) => `#${u.requestId} (${u.reason.replace(/_/g, ' ').toLowerCase()})`).join(', ')}. They stay approved for the next run.<//>`}
    ${routes.length > 0
      ? html`<div class="kpis">
            <div class="kpi k-green"><div class="v">${routes.length}</div><div class="l">routes</div></div>
            <div class="kpi k-blue"><div class="v">${stops}</div><div class="l">pickups planned</div></div>
            <div class="kpi"><div class="v">${km.toFixed(1)}</div><div class="l">km in total</div></div>
            ${result && html`<div class=${'kpi' + (result.unassigned.length ? ' k-amber' : '')}><div class="v">${result.unassigned.length}</div><div class="l">not planned</div></div>`}
          </div>
          <section class="card"><${RouteMap} routes=${routes} tall=${true} /></section>
          ${routes.map(
            (route, index) => html`<section class="card" key=${route.id}>
              <div class="page-head">
                <div class="route-title">
                  <span class="swatch" style=${{ background: COLORS[index % COLORS.length] }}></span>
                  <div>
                    <h2>Route ${route.id} · ${route.vehicleRegistration}</h2>
                    <p class="muted">Driver: ${route.driverName || 'none'} · ${route.totalDistanceKm} km · ${route.stops.length} stops</p>
                  </div>
                </div>
                <${Badge} kind=${route.status}>${route.status}<//>
              </div>
              <${StopList} route=${route} />
            </section>`,
          )}`
      : html`<section class="card empty">
          <span class="how-icon"><${Icon} name="route" /></span>
          <h3>No routes for this date yet</h3>
          <p class="muted">Approve some requests, then press Generate routes.</p>
        </section>`}
  `;
}
