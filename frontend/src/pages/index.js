// Every page of the app: its path, menu label and which roles may open it.
// `roles: null` means anyone, signed in or not. Paths may contain :params.
import Home from './Home.js';
import SubmitRequest from './requests/SubmitRequest.js';

export const pages = [
  { path: '/', component: Home, label: 'Home', roles: null, menu: false },
  { path: '/requests/new', component: SubmitRequest, label: 'Request pickup', roles: ['CITIZEN'] },
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
