import { post } from '../../api.js';
import MapPicker from '../../components/MapPicker.js';
import { Badge, html, Notice, useState, WASTE_TYPES } from '../../lib.js';

const MAX_PHOTO_BYTES = 5 * 1024 * 1024;

function readAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(new Error('Could not read the photo.'));
    reader.readAsDataURL(file);
  });
}

export default function SubmitRequest() {
  const [location, setLocation] = useState(null);
  const [wasteType, setWasteType] = useState('MIXED');
  const [quantity, setQuantity] = useState('');
  const [photo, setPhoto] = useState(null);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);
  const [created, setCreated] = useState(null);

  const pickPhoto = async (event) => {
    const file = event.target.files[0];
    setError('');
    if (!file) return setPhoto(null);
    if (file.size > MAX_PHOTO_BYTES) {
      event.target.value = '';
      return setError('The photo is larger than 5 MB. Please choose a smaller one.');
    }
    setPhoto(await readAsDataUrl(file));
  };

  const submit = async (event) => {
    event.preventDefault();
    setError('');
    if (!location) return setError('Please tap the map or search an address so we know where to collect.');
    if (!(Number(quantity) > 0)) return setError('Enter roughly how many kilograms there are.');
    setSaving(true);
    try {
      const result = await post('/requests', {
        latitude: location.latitude,
        longitude: location.longitude,
        address: location.address || null,
        wasteType,
        estimatedQuantityKg: Number(quantity),
        photo: photo ? photo.split(',', 2)[1] : null,
      });
      setCreated(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  if (created) {
    return html`
      <section class="card stack">
        <h2>Request #${created.id} received</h2>
        <p>
          Status <${Badge} kind=${created.status}>${created.status}<//> · Priority
          <${Badge} kind=${created.priority}>${created.priority}<//>
        </p>
        <p class="muted">You will get a notification each time its status changes.</p>
        <div class="actions">
          <a class="button" href="#/requests/mine">See my requests</a>
          <button class="ghost" onClick=${() => { setCreated(null); setLocation(null); setQuantity(''); setPhoto(null); }}>
            New request
          </button>
        </div>
      </section>
    `;
  }

  const hint = WASTE_TYPES.find((w) => w.value === wasteType);
  return html`
    <div class="page-head"><div><h1>Request a pickup</h1><p class="muted">Tell us where, what and how much.</p></div></div>
    <form class="card stack" onSubmit=${submit} noValidate>
      <${Notice} kind="error">${error}<//>
      <div>
        <label>Where is the waste?</label>
        <${MapPicker} value=${location} onChange=${setLocation} />
      </div>
      <div class="row">
        <div>
          <label for="waste">Type of waste</label>
          <select id="waste" value=${wasteType} onChange=${(e) => setWasteType(e.target.value)}>
            ${WASTE_TYPES.map((w) => html`<option key=${w.value} value=${w.value}>${w.label}</option>`)}
          </select>
          <p class="hint">${hint && hint.hint}</p>
        </div>
        <div>
          <label for="qty">Estimated quantity (kg)</label>
          <input id="qty" type="number" min="1" step="1" inputmode="decimal" value=${quantity}
            onInput=${(e) => setQuantity(e.target.value)} placeholder="e.g. 20" />
        </div>
      </div>
      <div>
        <label for="photo">Photo <span class="hint">(optional, up to 5 MB)</span></label>
        <input id="photo" type="file" accept="image/*" onChange=${pickPhoto} />
      </div>
      <div class="actions"><button type="submit" disabled=${saving}>${saving ? 'Sending…' : 'Submit request'}</button></div>
    </form>
  `;
}
