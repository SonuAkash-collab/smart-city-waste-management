import { post } from '../../api.js';
import { html, Notice, useState } from '../../lib.js';
import { saveSession } from '../../session.js';

export default function Register() {
  const [form, setForm] = useState({ fullName: '', email: '', password: '', confirm: '' });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const submit = async (event) => {
    event.preventDefault();
    setError('');
    if (form.password.length < 8) return setError('Use at least 8 characters for the password.');
    if (form.password !== form.confirm) return setError('The two passwords do not match.');
    setBusy(true);
    try {
      await post('/auth/register', { fullName: form.fullName, email: form.email, password: form.password });
      const login = await post('/auth/login', { email: form.email, password: form.password });
      saveSession(login.accessToken, login.user);
      window.location.hash = '/requests/new';
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return html`
    <section class="card stack" style=${{ maxWidth: '460px', margin: '2rem auto' }}>
      <h1>Create an account</h1>
      <p class="muted">Citizens can request pickups and follow their status.</p>
      <${Notice} kind="error">${error}<//>
      <form class="stack" onSubmit=${submit}>
        <div>
          <label for="name">Full name</label>
          <input id="name" required autocomplete="name" value=${form.fullName} onInput=${set('fullName')} />
        </div>
        <div>
          <label for="r-email">Email</label>
          <input id="r-email" type="email" required autocomplete="email" value=${form.email} onInput=${set('email')} />
        </div>
        <div class="row">
          <div>
            <label for="r-pass">Password <span class="hint">(8+ characters)</span></label>
            <input id="r-pass" type="password" required autocomplete="new-password" value=${form.password} onInput=${set('password')} />
          </div>
          <div>
            <label for="r-confirm">Repeat password</label>
            <input id="r-confirm" type="password" required autocomplete="new-password" value=${form.confirm} onInput=${set('confirm')} />
          </div>
        </div>
        <button type="submit" disabled=${busy}>${busy ? 'Creating…' : 'Create account'}</button>
      </form>
      <p class="muted">Already registered? <a href="#/login">Log in</a>.</p>
    </section>
  `;
}
