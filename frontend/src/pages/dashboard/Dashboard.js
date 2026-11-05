import { api, get } from '../../api.js';
import { html, Notice, todayIso, titleCase, useEffect, useState } from '../../lib.js';

function Tiles({ title, counts }) {
  return html`<section class="card"><h2>${title}</h2><div class="grid">
    ${Object.entries(counts).map(([key, value]) => html`<div key=${key}>
      <div class="hint">${titleCase(key)}</div><div style=${{ fontSize: '1.8rem', fontWeight: 700 }}>${value}</div>
    </div>`)}
  </div></section>`;
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
    <div class="page-head"><div><h1>Dashboard</h1><p class="muted">Live counts from the database.</p></div></div>
    <${Notice} kind="error">${error}<//>
    ${data && html`
      <${Tiles} title="Pending requests by priority" counts=${data.pendingByPriority} />
      <${Tiles} title="Requests by status" counts=${data.requestsByStatus} />
      <${Tiles} title="Vehicles" counts=${data.vehiclesByStatus} />
      <section class="card"><h2>Facility capacity today</h2>
        ${data.facilities.map((f) => html`<p key=${f.id}><strong>${f.name}</strong>: ${f.remainingCapacityKg} of ${f.dailyCapacityKg} kg left (${f.remainingPercent}%)</p>`)}
      </section>`}
    <section class="card row">
      <div><label for="d-day">Report date</label><input id="d-day" type="date" value=${day} onChange=${(e) => setDay(e.target.value)} /></div>
      <div style=${{ flex: '0 0 auto' }}><button onClick=${download}>Download CSV report</button></div>
    </section>
  `;
}
