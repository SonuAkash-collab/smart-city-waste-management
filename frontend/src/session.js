// The logged-in user's token and profile, kept in localStorage.
const TOKEN_KEY = 'scw.token';
const USER_KEY = 'scw.user';

function read(key) {
  try {
    return window.localStorage.getItem(key);
  } catch {
    return null;
  }
}

function write(key, value) {
  try {
    if (value === null) window.localStorage.removeItem(key);
    else window.localStorage.setItem(key, value);
  } catch {
    /* storage blocked: the session lasts until the page closes */
  }
}

let memoryToken = null;
let memoryUser = null;

export function getToken() {
  return read(TOKEN_KEY) || memoryToken;
}

export function getUser() {
  const raw = read(USER_KEY);
  if (raw) {
    try {
      return JSON.parse(raw);
    } catch {
      return null;
    }
  }
  return memoryUser;
}

export function saveSession(token, user) {
  memoryToken = token;
  memoryUser = user;
  write(TOKEN_KEY, token);
  write(USER_KEY, JSON.stringify(user));
  window.dispatchEvent(new Event('session-changed'));
}

export function clearSession() {
  memoryToken = null;
  memoryUser = null;
  write(TOKEN_KEY, null);
  write(USER_KEY, null);
  window.dispatchEvent(new Event('session-changed'));
}
