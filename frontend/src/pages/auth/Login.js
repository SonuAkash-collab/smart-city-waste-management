import { post } from '../../api.js';
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
    <section class="card stack" style=${{ maxWidth: '420px', margin: '2rem auto' }}>
      <h1>Log in</h1>
      <${Notice} kind="error">${error}<//>
      <form class="stack" onSubmit=${submit}>
        <div>
          <label for="email">Email</label>
          <input id="email" type="email" autocomplete="username" required value=${email}
            onInput=${(e) => setEmail(e.target.value)} />
        </div>
        <div>
          <label for="password">Password</label>
          <input id="password" type="password" autocomplete="current-password" required value=${password}
            onInput=${(e) => setPassword(e.target.value)} />
        </div>
        <button type="submit" disabled=${busy}>${busy ? 'Logging in…' : 'Log in'}</button>
      </form>
      <p class="muted">New here? <a href="#/register">Create a citizen account</a>.</p>
    </section>
  `;
}
