// Small wrapper around fetch for the /api/v1 backend.
// Adds the bearer token, sends and reads JSON, and turns the common
// error body {"error": {"code", "message"}} into an ApiError.
import { clearSession, getToken } from './session.js';

const BASE = '/api/v1';

export class ApiError extends Error {
  constructor(status, code, message, details) {
    super(message);
    this.status = status;
    this.code = code;
    this.details = details || [];
  }
}

export async function api(path, { method = 'GET', body, query, raw = false } = {}) {
  const url = new URL(BASE + path, window.location.origin);
  Object.entries(query || {}).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') url.searchParams.set(key, value);
  });
  const headers = { Accept: 'application/json' };
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  let response;
  try {
    response = await fetch(url, { method, headers, body: body === undefined ? undefined : JSON.stringify(body) });
  } catch {
    throw new ApiError(0, 'NETWORK', 'Cannot reach the server. Check that it is running.');
  }

  if (response.status === 401 && token) {
    // Expired, forged or deactivated token: start a fresh session.
    clearSession();
  }
  if (raw && response.ok) return response;

  const data = response.status === 204 ? null : await response.json().catch(() => null);
  if (!response.ok) {
    const error = (data && data.error) || {};
    throw new ApiError(response.status, error.code || 'ERROR', error.message || response.statusText, error.details);
  }
  return data;
}

export const get = (path, query) => api(path, { query });
export const post = (path, body) => api(path, { method: 'POST', body });
export const patch = (path, body) => api(path, { method: 'PATCH', body });
export const del = (path) => api(path, { method: 'DELETE' });
