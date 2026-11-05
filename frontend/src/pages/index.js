// Every page of the app: its path, menu label and which roles may open it.
// `roles: null` means anyone, signed in or not. Paths may contain :params.
// `group` and `icon` place the page in the sidebar menu.
import Staff from './admin/Staff.js';
import Login from './auth/Login.js';
import Register from './auth/Register.js';
import Facilities from './facilities/Facilities.js';
import Intake from './facilities/Intake.js';
import Vehicles from './fleet/Vehicles.js';
import Dashboard from './dashboard/Dashboard.js';
import Home from './Home.js';
import Notifications from './Notifications.js';
import AdminRoutes from './routes/AdminRoutes.js';
import DriverRoute from './routes/DriverRoute.js';
import AdminRequests from './requests/AdminRequests.js';
import MyRequests from './requests/MyRequests.js';
import RequestDetail from './requests/RequestDetail.js';
import SubmitRequest from './requests/SubmitRequest.js';

export const pages = [
  { path: '/', component: Home, label: 'Home', roles: null, menu: false },
  { path: '/login', component: Login, label: 'Log in', roles: null, guestOnly: true },
  { path: '/register', component: Register, label: 'Register', roles: null, guestOnly: true },
  { path: '/requests/mine', component: MyRequests, label: 'My requests', roles: ['CITIZEN'], group: 'Pickups', icon: 'inbox' },
  { path: '/requests/new', component: SubmitRequest, label: 'Request pickup', roles: ['CITIZEN'], group: 'Pickups', icon: 'plus' },
  { path: '/requests/:id', component: RequestDetail, label: 'Request', roles: ['CITIZEN', 'ADMIN'], menu: false },
  { path: '/admin/dashboard', component: Dashboard, label: 'Dashboard', roles: ['ADMIN'], group: 'Overview', icon: 'chart' },
  { path: '/admin/requests', component: AdminRequests, label: 'Requests', roles: ['ADMIN'], group: 'Operations', icon: 'inbox' },
  { path: '/admin/routes', component: AdminRoutes, label: 'Routes', roles: ['ADMIN'], group: 'Operations', icon: 'route' },
  { path: '/driver/route', component: DriverRoute, label: 'My route', roles: ['DRIVER'], group: 'Today', icon: 'navigation' },
  { path: '/admin/vehicles', component: Vehicles, label: 'Vehicles', roles: ['ADMIN'], group: 'Resources', icon: 'truck' },
  { path: '/admin/facilities', component: Facilities, label: 'Facilities', roles: ['ADMIN'], group: 'Resources', icon: 'factory' },
  { path: '/admin/staff', component: Staff, label: 'Staff', roles: ['ADMIN'], group: 'Resources', icon: 'users' },
  { path: '/operator/intake', component: Intake, label: 'Record delivery', roles: ['OPERATOR'], group: 'Facility', icon: 'scale' },
  { path: '/notifications', component: Notifications, label: 'Notifications', roles: ['CITIZEN', 'DRIVER', 'ADMIN', 'OPERATOR'], group: 'Account', icon: 'bell' },
];

function match(pattern, path) {
  const want = pattern.split('/').filter(Boolean);
  const have = path.split('/').filter(Boolean);
  if (want.length !== have.length) return null;
  const params = {};
  for (let i = 0; i < want.length; i += 1) {
    if (want[i].startsWith(':')) params[want[i].slice(1)] = decodeURIComponent(have[i]);
    else if (want[i] !== have[i]) return null;
  }
  return params;
}

export function findPage(path) {
  for (const page of pages) {
    const params = match(page.path, path);
    if (params) return { page, params };
  }
  return null;
}
