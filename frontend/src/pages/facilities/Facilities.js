import { get, post } from '../../api.js';
import { html, Notice, useEffect, useState, WASTE_TYPES } from '../../lib.js';

const EMPTY = { name: '', latitude: '', longitude: '', acceptedWasteTypes: ['MIXED'], dailyCapacityKg: '' };

function CapacityBar({ percent }) {
  const color = percent < 15 ? 'var(--red)' : percent < 40 ? 'var(--amber)' : 'var(--green)';
  return html`<div style=${{ background: 'var(--line)', borderRadius: '6px', height: '8px', minWidth: '120px' }}>
    <div style=${{ width: `${percent}%`, background: color, height: '8px', borderRadius: '6px' }}></div>
  </div>`;
}

export default function Facilities() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [msg, setMsg] = useState({ kind: 'info', text: '' });
  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value });
  const load = () => get('/facilities').then(setItems).catch((err) => setMsg({ kind: 'error', text: err.message }));
  useEffect(() => {
    load();
  }, []);

  const toggle = (value) => {
    const list = form.acceptedWasteTypes;
    setForm({ ...form, acceptedWasteTypes: list.includes(value) ? list.filter((w) => w !== value) : [...list, value] });
  };
  const add = async (e) => {
    e.preventDefault();
    try {
      await post('/facilities', { ...form, latitude: Number(form.latitude), longitude: Number(form.longitude), dailyCapacityKg: Number(form.dailyCapacityKg) });
      setMsg({ kind: 'success', text: `${form.name} added.` });
      setForm(EMPTY);
      load();
    } catch (err) {
      setMsg({ kind: 'error', text: err.message });
    }
  };

  return html`
    <div class="page-head"><div><h1>Disposal facilities</h1><p class="muted">Remaining capacity today. Full facilities are skipped when routes are planned.</p></div></div>
    <${Notice} kind=${msg.kind}>${msg.text}<//>
    <section class="card">
      <table class="responsive">
        <thead><tr><th>Facility</th><th>Accepts</th><th>Remaining today</th><th></th></tr></thead>
        <tbody>
          ${items.map((f) => html`<tr key=${f.id}>
            <td data-label="Facility"><strong>${f.name}</strong> <span class="hint">ID ${f.id}</span></td>
            <td data-label="Accepts">${f.acceptedWasteTypes.join(', ')}</td>
            <td data-label="Remaining">${f.remainingCapacityKg} of ${f.dailyCapacityKg} kg (${f.remainingPercent}%)</td>
            <td data-label=""><${CapacityBar} percent=${f.remainingPercent} /></td>
          </tr>`)}
        </tbody>
      </table>
    </section>
    <form class="card stack" onSubmit=${add}>
      <h2>Add facility</h2>
      <div class="row">
        <div><label for="f-name">Name</label><input id="f-name" required value=${form.name} onInput=${set('name')} /></div>
        <div><label for="f-lat">Latitude</label><input id="f-lat" required value=${form.latitude} onInput=${set('latitude')} /></div>
        <div><label for="f-lon">Longitude</label><input id="f-lon" required value=${form.longitude} onInput=${set('longitude')} /></div>
        <div><label for="f-cap">Daily capacity (kg)</label><input id="f-cap" type="number" min="1" required value=${form.dailyCapacityKg} onInput=${set('dailyCapacityKg')} /></div>
      </div>
      <div class="actions">
        ${WASTE_TYPES.map((w) => html`<label key=${w.value} class="hint" style=${{ fontWeight: 400 }}>
          <input type="checkbox" style=${{ width: 'auto' }} checked=${form.acceptedWasteTypes.includes(w.value)} onChange=${() => toggle(w.value)} /> ${w.label}
        </label>`)}
      </div>
      <div class="actions"><button type="submit">Add facility</button></div>
    </form>
  `;
}
