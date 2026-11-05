import { get, post } from '../../api.js';
import { html, Notice, useEffect, useState, WASTE_TYPES } from '../../lib.js';

export default function Intake() {
  const [facilities, setFacilities] = useState([]);
  const [vehicles, setVehicles] = useState([]);
  const [form, setForm] = useState({ facilityId: '', vehicleId: '', wasteType: 'MIXED', weightKg: '' });
  const [msg, setMsg] = useState({ kind: 'info', text: '' });
  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const load = () => {
    get('/facilities').then((list) => {
      setFacilities(list);
      if (list.length && !form.facilityId) setForm((f) => ({ ...f, facilityId: String(list[0].id) }));
    });
    get('/vehicles/').then(setVehicles).catch(() => setVehicles([]));
  };
  useEffect(load, []);

  const facility = facilities.find((f) => String(f.id) === form.facilityId);
  const record = async (e) => {
    e.preventDefault();
    try {
      const result = await post(`/facilities/${form.facilityId}/intakes`, {
        vehicleId: Number(form.vehicleId),
        wasteType: form.wasteType,
        weightKg: Number(form.weightKg),
      });
      setMsg({ kind: 'success', text: `Recorded ${result.weightKg} kg. ${result.remainingCapacityKg} kg left today.` });
      setForm({ ...form, weightKg: '' });
      load();
    } catch (err) {
      setMsg({ kind: 'error', text: err.message });
    }
  };

  return html`
    <div class="page-head"><div><h1>Record a delivery</h1><p class="muted">Each delivery lowers today's remaining capacity.</p></div></div>
    <${Notice} kind=${msg.kind}>${msg.text}<//>
    <form class="card stack" onSubmit=${record}>
      <div class="row">
        <div>
          <label for="i-fac">Facility</label>
          <select id="i-fac" value=${form.facilityId} onChange=${set('facilityId')}>
            ${facilities.map((f) => html`<option key=${f.id} value=${f.id}>${f.name}</option>`)}
          </select>
          ${facility && html`<p class="hint">${facility.remainingCapacityKg} kg left today · accepts ${facility.acceptedWasteTypes.join(', ')}</p>`}
        </div>
        <div>
          <label for="i-veh">Vehicle</label>
          <select id="i-veh" required value=${form.vehicleId} onChange=${set('vehicleId')}>
            <option value="">Choose…</option>
            ${vehicles.map((v) => html`<option key=${v.id} value=${v.id}>${v.registrationNumber}</option>`)}
          </select>
        </div>
      </div>
      <div class="row">
        <div>
          <label for="i-type">Waste type</label>
          <select id="i-type" value=${form.wasteType} onChange=${set('wasteType')}>
            ${WASTE_TYPES.map((w) => html`<option key=${w.value} value=${w.value}>${w.label}</option>`)}
          </select>
        </div>
        <div><label for="i-kg">Weight (kg)</label><input id="i-kg" type="number" min="0.1" step="0.1" required value=${form.weightKg} onInput=${set('weightKg')} /></div>
      </div>
      <div class="actions"><button type="submit">Record delivery</button></div>
    </form>
  `;
}
