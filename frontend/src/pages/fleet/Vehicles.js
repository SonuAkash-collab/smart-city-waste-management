import { get, patch, post } from '../../api.js';
import Icon from '../../components/Icon.js';
import { Badge, html, Notice, useEffect, useState, WASTE_TYPES } from '../../lib.js';

const EMPTY = { registrationNumber: '', capacityKg: '', wasteTypes: ['MIXED'], depotLatitude: '12.9300', depotLongitude: '77.5400' };

export default function Vehicles() {
  const [vehicles, setVehicles] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [msg, setMsg] = useState({ kind: 'info', text: '' });
  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value });
  const fail = (err) => setMsg({ kind: 'error', text: err.message });

  const load = () => {
    get('/vehicles/').then(setVehicles).catch(fail);
    get('/users', { role: 'DRIVER' }).then(setDrivers).catch(fail);
  };
  useEffect(load, []);

  const toggleType = (value) => {
    const has = form.wasteTypes.includes(value);
    setForm({ ...form, wasteTypes: has ? form.wasteTypes.filter((w) => w !== value) : [...form.wasteTypes, value] });
  };

  const add = async (e) => {
    e.preventDefault();
    try {
      await post('/vehicles/', { ...form, capacityKg: Number(form.capacityKg), depotLatitude: Number(form.depotLatitude), depotLongitude: Number(form.depotLongitude) });
      setMsg({ kind: 'success', text: `Vehicle ${form.registrationNumber.toUpperCase()} added.` });
      setForm(EMPTY);
      load();
    } catch (err) {
      fail(err);
    }
  };
  const change = (id, body) => patch(`/vehicles/${id}`, body).then(load).catch(fail);
  const assign = (id, driverId) => driverId && patch(`/vehicles/${id}/driver`, { driverId: Number(driverId) }).then(load).catch(fail);

  const count = (status) => vehicles.filter((v) => v.status === status).length;
  return html`
    <div class="page-head"><div><span class="eyebrow">Resources</span><h1>Vehicles</h1><p class="muted">Fleet, capacity, status and drivers.</p></div></div>
    ${vehicles.length > 0 && html`<div class="kpis">
      <div class="kpi"><div class="v">${vehicles.length}</div><div class="l">Vehicles</div></div>
      <div class="kpi k-green"><div class="v">${count('AVAILABLE')}</div><div class="l">Available</div></div>
      <div class="kpi k-blue"><div class="v">${count('ON_ROUTE')}</div><div class="l">On route</div></div>
      <div class="kpi k-amber"><div class="v">${count('MAINTENANCE')}</div><div class="l">In maintenance</div></div>
      <div class="kpi"><div class="v">${vehicles.filter((v) => !v.driverId).length}</div><div class="l">Without a driver</div></div>
    </div>`}
    <${Notice} kind=${msg.kind}>${msg.text}<//>
    <section class="card">
      <table class="responsive">
        <thead><tr><th>Vehicle</th><th>Capacity / load</th><th>Waste types</th><th>Status</th><th>Driver</th></tr></thead>
        <tbody>
          ${vehicles.map((v) => html`<tr key=${v.id}>
            <td data-label="Vehicle"><span class="veh"><span class="veh-icon"><${Icon} name="truck" /></span><span><strong>${v.registrationNumber}</strong><br /><span class="hint">ID ${v.id}</span></span></span></td>
            <td data-label="Capacity">
              <span class="num">${v.currentLoadKg} / ${v.capacityKg} kg</span>
              <div class=${'bar' + (v.currentLoadKg / v.capacityKg > 0.85 ? ' bad' : v.currentLoadKg / v.capacityKg > 0.6 ? ' warn' : '')} style=${{ marginTop: '0.3rem' }}>
                <span style=${{ width: `${Math.min(100, (100 * v.currentLoadKg) / v.capacityKg)}%` }}></span>
              </div>
            </td>
            <td data-label="Waste">${v.wasteTypes.join(', ')}</td>
            <td data-label="Status">
              ${v.status === 'ON_ROUTE'
                ? html`<${Badge} kind="on_route">ON ROUTE<//>`
                : html`<select value=${v.status} onChange=${(e) => change(v.id, { status: e.target.value })}>
                    <option value="AVAILABLE">Available</option><option value="MAINTENANCE">Maintenance</option>
                  </select>`}
            </td>
            <td data-label="Driver">
              <select value=${v.driverId || ''} onChange=${(e) => assign(v.id, e.target.value)}>
                <option value="">No driver</option>
                ${drivers.map((d) => html`<option key=${d.id} value=${d.id}>${d.fullName}</option>`)}
              </select>
            </td>
          </tr>`)}
        </tbody>
      </table>
    </section>
    <form class="card stack" onSubmit=${add}>
      <h2>Add vehicle</h2>
      <div class="row">
        <div><label for="v-reg">Registration number</label><input id="v-reg" required value=${form.registrationNumber} onInput=${set('registrationNumber')} /></div>
        <div><label for="v-cap">Capacity (kg)</label><input id="v-cap" type="number" min="1" required value=${form.capacityKg} onInput=${set('capacityKg')} /></div>
        <div><label for="v-lat">Depot latitude</label><input id="v-lat" value=${form.depotLatitude} onInput=${set('depotLatitude')} /></div>
        <div><label for="v-lon">Depot longitude</label><input id="v-lon" value=${form.depotLongitude} onInput=${set('depotLongitude')} /></div>
      </div>
      <div>
        <label>Waste types it can carry</label>
        <div class="actions">
          ${WASTE_TYPES.map((w) => html`<label key=${w.value} class="hint" style=${{ fontWeight: 400 }}>
            <input type="checkbox" style=${{ width: 'auto' }} checked=${form.wasteTypes.includes(w.value)} onChange=${() => toggleType(w.value)} /> ${w.label}
          </label>`)}
        </div>
      </div>
      <div class="actions"><button type="submit">Add vehicle</button></div>
    </form>
  `;
}
