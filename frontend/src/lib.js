// React, htm and Leaflet are loaded as plain <script> files in index.html.
// This module gives the rest of the app one place to import them from.
const { React, ReactDOM, htm, L } = window;

export const html = htm.bind(React.createElement);
export const { useState, useEffect, useMemo, useRef, useCallback, Fragment } = React;
export { React, ReactDOM, L };

export const WASTE_TYPES = [
  { value: 'HAZARDOUS', label: 'Hazardous', hint: 'Chemicals, paint, batteries' },
  { value: 'MEDICAL', label: 'Medical', hint: 'Syringes, medicines, dressings' },
  { value: 'E_WASTE', label: 'E-waste', hint: 'Phones, cables, small appliances' },
  { value: 'MIXED', label: 'Mixed household', hint: 'Everyday household waste' },
  { value: 'RECYCLABLE', label: 'Recyclable', hint: 'Paper, plastic, glass, metal' },
  { value: 'GARDEN', label: 'Garden', hint: 'Leaves, branches, grass' },
  { value: 'BULKY', label: 'Bulky', hint: 'Furniture, mattresses' },
];

export const STATUSES = ['SUBMITTED', 'APPROVED', 'SCHEDULED', 'COLLECTED', 'REJECTED', 'MISSED', 'CANCELLED'];
export const PRIORITIES = ['HIGH', 'MEDIUM', 'LOW'];

export function wasteLabel(value) {
  const found = WASTE_TYPES.find((w) => w.value === value);
  return found ? found.label : value;
}

export function titleCase(value) {
  return (value || '').replace(/_/g, ' ').toLowerCase().replace(/^\w/, (c) => c.toUpperCase());
}

export function formatDateTime(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleString(undefined, { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
}

export function todayIso() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

export function Badge({ kind, children }) {
  return html`<span class=${`badge badge-${String(kind || '').toLowerCase()}`}>${children}</span>`;
}

export function Notice({ kind = 'info', children }) {
  if (!children) return null;
  return html`<div class=${`notice notice-${kind}`} role=${kind === 'error' ? 'alert' : 'status'}>${children}</div>`;
}
