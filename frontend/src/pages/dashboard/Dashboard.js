import { api, get } from '../../api.js';
import Icon from '../../components/Icon.js';
import { html, Notice, todayIso, titleCase, useEffect, useState } from '../../lib.js';

// Colour of each count, so the same status always looks the same.
const TONE = {
  HIGH: 'red', MEDIUM: 'amber', LOW: 'grey',
  SUBMITTED: 'amber', APPROVED: 'blue', SCHEDULED: 'blue', COLLECTED: 'green',
  REJECTED: 'red', MISSED: 'red', CANCELLED: 'grey',
  AVAILABLE: 'green', ON_ROUTE: 'blue', MAINTENANCE: 'amber',
};
const COLOUR = { red: '#b8322a', amber: '#e39a1c', blue: '#1f5d9e', green: '#1d6b47', grey: '#9aa7a1' };

function Strip({ title, counts }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  return html`
    <div class="kpi-title"><h2>${title}</h2><span class="hint">${total} in total</span></div>
    <div class="kpis">
      ${Object.entries(counts).map(
        ([key, value]) => html`<div key=${key} class=${'kpi k-' + (TONE[key] || 'grey') + (value === 0 ? ' zero' : '')}>
          <div class="v">${value}</div><div class="l">${titleCase(key)}</div>
        </div>`,
      )}
    </div>
  `;
}

// One bar split by status: a quick picture of where all requests are.
function StatusBar({ counts }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  const parts = Object.entries(counts).filter(([, v]) => v > 0);
  return html`<section class="card">
    <h2>Where requests are</h2>
    <div class="stack-bar" role="img" aria-label="Requests by status">
      ${parts.map(([key, value]) => html`<span key=${key} title=${`${titleCase(key)}: ${value}`}
        style=${{ width: `${(100 * value) / total}%`, background: COLOUR[TONE[key] || 'grey'] }}></span>`)}
    </div>
    <div class="legend">
      ${parts.map(([key, value]) => html`<span key=${key}><i style=${{ background: COLOUR[TONE[key] || 'grey'] }}></i>${titleCase(key)} ${value}</span>`)}
    </div>
  </section>`;
}

function Capacity({ facilities }) {
  return html`<section class="card">
    <h2>Facility capacity today</h2>
    ${facilities.map((f) => {
      const tone = f.remainingPercent < 15 ? 'bad' : f.remainingPercent < 40 ? 'warn' : '';
      return html`<div key=${f.id} class="cap-row">
        <strong>${f.name}</strong>
        <div class=${'bar lg ' + tone}><span style=${{ width: `${f.remainingPercent}%` }}></span></div>
        <span class="num">${f.remainingCapacityKg} / ${f.dailyCapacityKg} kg left</span>
      </div>`;
    })}
  </section>`;
}

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [day, setDay] = useState(todayIso());
  const [error, setError] = useState('');
  useEffect(() => {
    get('/dashboard').then(setData).catch((err) => setError(err.message));
  }, []);

  const download = async () => {
    setError('');
    try {
      const response = await api('/reports/daily.csv', { query: { date: day }, raw: true });
      const url = URL.createObjectURL(await response.blob());
      const link = Object.assign(document.createElement('a'), { href: url, download: `collection-report-${day}.csv` });
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message);
    }
  };

  return html`
    <div class="page-head">
      <div><span class="eyebrow">Overview</span><h1>Dashboard</h1><p class="muted">Live counts from the database.</p></div>
      <div class="actions">
        <input aria-label="Report date" type="date" value=${day} onChange=${(e) => setDay(e.target.value)} style=${{ width: 'auto' }} />
        <button onClick=${download}><${Icon} name="list" /> Download CSV report</button>
      </div>
    </div>
    <${Notice} kind="error">${error}<//>
    ${!data
      ? !error && html`<p class="muted">Loading…</p>`
      : html`
        <${Strip} title="Pending requests by priority" counts=${data.pendingByPriority} />
        <${StatusBar} counts=${data.requestsByStatus} />
        <${Strip} title="Requests by status" counts=${data.requestsByStatus} />
        <div class="split">
          <${Capacity} facilities=${data.facilities} />
          <section class="card">
            <h2>Vehicles</h2>
            ${Object.entries(data.vehiclesByStatus).map(([key, value]) => html`<div key=${key} class="cap-row" style=${{ gridTemplateColumns: '1fr auto' }}>
              <span><span class=${'badge badge-' + key.toLowerCase()}>${titleCase(key)}</span></span>
              <strong class="num" style=${{ fontSize: '1.3rem' }}>${value}</strong>
            </div>`)}
          </section>
        </div>`}
  `;
}
