import { html, L, useEffect, useRef, useState } from '../lib.js';

export const CITY_CENTER = [12.9716, 77.5946]; // Bengaluru
const TILE_URL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';

export function baseMap(element, center = CITY_CENTER, zoom = 13) {
  const map = L.map(element, { scrollWheelZoom: false }).setView(center, zoom);
  L.tileLayer(TILE_URL, { maxZoom: 19, attribution: ATTRIBUTION }).addTo(map);
  return map;
}

// Search an address with OpenStreetMap Nominatim (the Map Service in the SAD).
export async function geocode(address) {
  const url = new URL('https://nominatim.openstreetmap.org/search');
  url.searchParams.set('format', 'json');
  url.searchParams.set('limit', '1');
  url.searchParams.set('q', address);
  const response = await fetch(url, { headers: { Accept: 'application/json' } });
  if (!response.ok) throw new Error('Address search is not available right now.');
  const results = await response.json();
  if (!results.length) return null;
  return { latitude: Number(results[0].lat), longitude: Number(results[0].lon), label: results[0].display_name };
}

// A map where the user drops a pin by tapping, searching an address or using GPS.
export default function MapPicker({ value, onChange }) {
  const holder = useRef(null);
  const mapRef = useRef(null);
  const markerRef = useRef(null);
  const [query, setQuery] = useState('');
  const [message, setMessage] = useState('');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    const map = baseMap(holder.current);
    map.on('click', (event) => onChange({ latitude: event.latlng.lat, longitude: event.latlng.lng }));
    mapRef.current = map;
    setTimeout(() => map.invalidateSize(), 50);
    return () => map.remove();
  }, []);

  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    if (!value) {
      if (markerRef.current) markerRef.current.remove();
      markerRef.current = null;
      return;
    }
    const point = [value.latitude, value.longitude];
    if (!markerRef.current) {
      markerRef.current = L.marker(point, { draggable: true }).addTo(map);
      markerRef.current.on('dragend', () => {
        const p = markerRef.current.getLatLng();
        onChange({ ...value, latitude: p.lat, longitude: p.lng });
      });
    } else {
      markerRef.current.setLatLng(point);
    }
    map.panTo(point);
  }, [value && value.latitude, value && value.longitude]);

  const search = async () => {
    if (!query.trim()) return;
    setBusy(true);
    setMessage('');
    try {
      const found = await geocode(query.trim());
      if (!found) setMessage('No match for that address. Try adding the area or city, or tap the map.');
      else {
        onChange({ latitude: found.latitude, longitude: found.longitude, address: query.trim() });
        mapRef.current.setView([found.latitude, found.longitude], 16);
      }
    } catch (error) {
      setMessage(error.message);
    } finally {
      setBusy(false);
    }
  };

  const locate = () => {
    if (!navigator.geolocation) {
      setMessage('This browser cannot share its location.');
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        onChange({ latitude: pos.coords.latitude, longitude: pos.coords.longitude, address: value && value.address });
        mapRef.current.setView([pos.coords.latitude, pos.coords.longitude], 17);
      },
      () => setMessage('Location permission was refused. Tap the map instead.'),
    );
  };

  return html`
    <div class="stack">
      <div class="row">
        <div>
          <label for="address">Address <span class="hint">(optional if you tap the map)</span></label>
          <input
            id="address"
            value=${query}
            placeholder="House, street, area"
            onInput=${(e) => {
              setQuery(e.target.value);
              if (value) onChange({ ...value, address: e.target.value });
            }}
            onKeyDown=${(e) => e.key === 'Enter' && (e.preventDefault(), search())}
          />
        </div>
        <div class="actions" style=${{ flex: '0 0 auto' }}>
          <button type="button" class="ghost" onClick=${search} disabled=${busy}>Find</button>
          <button type="button" class="ghost" onClick=${locate}>Use my location</button>
        </div>
      </div>
      <div ref=${holder} class="map" aria-label="Map: tap to place the pickup pin"></div>
      ${value
        ? html`<p class="hint">Pin at ${value.latitude.toFixed(5)}, ${value.longitude.toFixed(5)}. Drag it to adjust.</p>`
        : html`<p class="hint">Tap the map where the waste should be picked up.</p>`}
      ${message && html`<p class="hint" role="status">${message}</p>`}
    </div>
  `;
}
