import { baseMap } from './MapPicker.js';
import { html, L, useEffect, useRef } from '../lib.js';

const COLORS = ['#1f7a4d', '#1d5fa8', '#b45309', '#7c3aed', '#be123c', '#0f766e'];

function stopIcon(stop, color) {
  const done = stop.status !== 'PENDING';
  const label = stop.stopType === 'FACILITY' ? 'F' : String(stop.sequence);
  const background = stop.status === 'MISSED' ? '#b42318' : done ? '#8a9690' : color;
  return L.divIcon({
    className: 'stop-pin',
    html: `<span style="background:${background}">${label}</span>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });
}

// Draws one or more routes: a numbered pin per stop and a line in visiting order.
export default function RouteMap({ routes, tall = false }) {
  const holder = useRef(null);
  const mapRef = useRef(null);
  const layerRef = useRef(null);

  useEffect(() => {
    mapRef.current = baseMap(holder.current);
    layerRef.current = L.layerGroup().addTo(mapRef.current);
    setTimeout(() => mapRef.current.invalidateSize(), 50);
    return () => mapRef.current.remove();
  }, []);

  useEffect(() => {
    const layer = layerRef.current;
    layer.clearLayers();
    const bounds = [];
    (routes || []).forEach((route, index) => {
      const color = COLORS[index % COLORS.length];
      const points = route.stops.map((s) => [s.latitude, s.longitude]);
      if (points.length > 1) L.polyline(points, { color, weight: 4, opacity: 0.7 }).addTo(layer);
      route.stops.forEach((stop) => {
        const title = stop.stopType === 'FACILITY'
          ? `Unload at ${stop.facilityName}`
          : `#${stop.requestId} · ${stop.wasteType} · ${stop.quantityKg} kg`;
        L.marker([stop.latitude, stop.longitude], { icon: stopIcon(stop, color), title })
          .bindPopup(`<strong>Stop ${stop.sequence}</strong><br>${title}<br>${stop.address || ''}<br>Status: ${stop.status}`)
          .addTo(layer);
        bounds.push([stop.latitude, stop.longitude]);
      });
    });
    if (bounds.length) mapRef.current.fitBounds(bounds, { padding: [30, 30], maxZoom: 16 });
  }, [routes]);

  return html`<div ref=${holder} class=${'map' + (tall ? ' tall' : '')} aria-label="Route map with numbered stops"></div>`;
}
