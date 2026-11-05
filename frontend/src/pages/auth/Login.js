import { post } from '../../api.js';
import Icon from '../../components/Icon.js';
import { html, Notice, useState } from '../../lib.js';
import { saveSession } from '../../session.js';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async (event) => {
    event.preventDefault();
    setError('');
    setBusy(true);
    try {
      const result = await post('/auth/login', { email, password });
      saveSession(result.accessToken, result.user);
      window.location.hash = '/';
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return html`
    <section class="auth">
      <${AuthAside} />
      <div class="auth-form">
        <span class="eyebrow">Welcome back</span>
        <h1>Log in</h1>
        <p class="muted">Citizens, city staff, drivers and operators all log in here.</p>
        <${Notice} kind="error">${error}<//>
        <form class="stack" onSubmit=${submit}>
          <div>
            <label for="email">Email</label>
            <input id="email" type="email" autocomplete="username" required value=${email}
              placeholder="you@example.com" onInput=${(e) => setEmail(e.target.value)} />
          </div>
          <div>
            <label for="password">Password</label>
            <input id="password" type="password" autocomplete="current-password" required value=${password}
              onInput=${(e) => setPassword(e.target.value)} />
          </div>
          <button type="submit" class="big" disabled=${busy}>${busy ? 'Logging in…' : 'Log in'}</button>
        </form>
        <p class="muted">New here? <a href="#/register">Create a citizen account</a>.</p>
      </div>
    </section>
  `;
}

// The dark panel beside the log in and register forms.
export function AuthAside() {
  return html`<div class="auth-aside" aria-hidden="true">
    <span class="mark"><${Icon} name="recycle" size="22px" /></span>
    <h2>Every pickup, on one map.</h2>
    <ul>
      <li><${Icon} name="pin" /> Request a pickup in under a minute</li>
      <li><${Icon} name="route" /> Routes planned by priority and distance</li>
      <li><${Icon} name="bell" /> A notification at every status change</li>
    </ul>
  </div>`;
}
