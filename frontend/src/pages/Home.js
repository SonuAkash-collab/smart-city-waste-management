import Icon from '../components/Icon.js';
import { html } from '../lib.js';
import { getUser } from '../session.js';

const STEPS = [
  ['pin', 'Request', 'Drop a pin, pick the waste type and the weight. Add a photo if it helps.'],
  ['shield', 'Approve & prioritise', 'The city checks each request. Hazardous and medical waste goes first.'],
  ['route', 'Plan routes', 'Vehicles take turns picking the nearest high-priority stop that still fits their load.'],
  ['check', 'Collect & track', 'Drivers mark each stop. Citizens see every status change as it happens.'],
];

const ROLES = [
  ['inbox', 'Citizens', 'Request pickups and follow them to collection.'],
  ['chart', 'City admins', 'Approve requests, generate routes, watch capacity.'],
  ['navigation', 'Drivers', 'One clear list of stops with a map, on the phone.'],
  ['scale', 'Facility operators', 'Record deliveries so routes skip full sites.'],
];

// Quick links shown after logging in, per role.
const SHORTCUTS = {
  CITIZEN: [
    ['plus', '#/requests/new', 'Request a pickup', 'Tell us where, what and how much.'],
    ['inbox', '#/requests/mine', 'My requests', 'See the status of every request.'],
    ['bell', '#/notifications', 'Notifications', 'Updates on your pickups.'],
  ],
  ADMIN: [
    ['chart', '#/admin/dashboard', 'Dashboard', 'Live counts and the daily report.'],
    ['inbox', '#/admin/requests', 'Review requests', 'Approve, reject or re-prioritise.'],
    ['route', '#/admin/routes', 'Plan routes', 'Generate today’s collection routes.'],
    ['truck', '#/admin/vehicles', 'Vehicles', 'Fleet status and drivers.'],
  ],
  DRIVER: [
    ['navigation', '#/driver/route', 'My route', 'Your stops for today, in order.'],
    ['bell', '#/notifications', 'Notifications', 'New routes and changes.'],
  ],
  OPERATOR: [
    ['scale', '#/operator/intake', 'Record a delivery', 'Log what arrived at the facility.'],
    ['bell', '#/notifications', 'Notifications', 'Messages from the city.'],
  ],
};

// A small picture of a planned route, drawn with plain HTML and SVG.
function RoutePreview() {
  const stops = [
    ['1', 'Hazardous · 12 kg', 'HIGH'],
    ['2', 'E-waste · 30 kg', 'MEDIUM'],
    ['F', 'Unload at depot', ''],
    ['3', 'Garden · 50 kg', 'LOW'],
  ];
  return html`<div class="route-preview" aria-hidden="true">
    <div class="rp-head"><span class="badge badge-on_route">On route</span><span class="hint">KA-01 · 18.4 km</span></div>
    <svg class="rp-map" viewBox="0 0 320 150">
      <path d="M0 40 H320 M0 110 H320 M80 0 V150 M210 0 V150" stroke="#2a4a3f" stroke-width="10" fill="none" />
      <path d="M30 120 C 80 120, 70 50, 120 45 S 190 90, 230 60 S 280 20, 295 35" stroke="#c5ec3f" stroke-width="4"
        stroke-dasharray="8 7" fill="none" stroke-linecap="round" />
      <circle cx="30" cy="120" r="9" fill="#c5ec3f" /><circle cx="120" cy="45" r="9" fill="#fff" />
      <circle cx="230" cy="60" r="9" fill="#fff" /><circle cx="295" cy="35" r="9" fill="#fff" />
    </svg>
    <ol class="rp-stops">
      ${stops.map(
        ([n, text, priority]) => html`<li key=${n}>
          <span class=${'rp-n' + (n === 'F' ? ' f' : '')}>${n}</span><span>${text}</span>
          ${priority && html`<span class=${'badge badge-' + priority.toLowerCase()}>${priority}</span>`}
        </li>`,
      )}
    </ol>
  </div>`;
}

function Welcome({ user }) {
  const links = SHORTCUTS[user.role] || [];
  return html`
    <div class="page-head">
      <div>
        <span class="eyebrow">${user.role.toLowerCase()}</span>
        <h1>Hello, ${user.fullName.split(' ')[0]}</h1>
        <p class="muted">What would you like to do?</p>
      </div>
    </div>
    <div class="tiles">
      ${links.map(
        ([icon, href, title, text]) => html`<a key=${href} class="tile" href=${href}>
          <span class="tile-icon"><${Icon} name=${icon} /></span>
          <strong>${title}</strong><span class="muted">${text}</span>
          <span class="tile-go"><${Icon} name="arrow" /></span>
        </a>`,
      )}
    </div>
  `;
}

export default function Home() {
  const user = getUser();
  if (user) return html`<${Welcome} user=${user} />`;
  return html`
    <section class="landing">
      <div class="landing-copy">
        <span class="eyebrow">Smart City · Waste Management</span>
        <h1>Cleaner streets, planned smarter.</h1>
        <p class="lead">
          Request a waste pickup, follow it from approval to collection, and let the city plan
          the shortest safe routes for its vehicles.
        </p>
        <div class="actions">
          <a class="button big" href="#/register">Request a pickup <${Icon} name="arrow" /></a>
          <a class="button ghost big" href="#/login">Log in</a>
        </div>
        <ul class="facts">
          <li><strong>Priority first</strong><span>Hazardous and medical waste is collected before anything else.</span></li>
          <li><strong>Capacity aware</strong><span>Routes respect vehicle loads and facility limits.</span></li>
        </ul>
      </div>
      <${RoutePreview} />
    </section>

    <section class="how">
      <h2>How it works</h2>
      <ol class="how-steps">
        ${STEPS.map(
          ([icon, title, text], i) => html`<li key=${title}>
            <span class="how-icon"><${Icon} name=${icon} /></span>
            <span class="hint">Step ${i + 1}</span>
            <strong>${title}</strong>
            <p class="muted">${text}</p>
          </li>`,
        )}
      </ol>
    </section>

    <section class="how">
      <h2>One system, four roles</h2>
      <div class="role-grid">
        ${ROLES.map(
          ([icon, title, text]) => html`<div key=${title} class="role-card">
            <${Icon} name=${icon} /><strong>${title}</strong><span class="muted">${text}</span>
          </div>`,
        )}
      </div>
    </section>
  `;
}
