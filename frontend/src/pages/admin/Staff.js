import { get, patch, post } from '../../api.js';
import { Badge, html, Notice, useEffect, useState } from '../../lib.js';

const EMPTY = { fullName: '', email: '', role: 'DRIVER', temporaryPassword: '' };

export default function Staff() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [message, setMessage] = useState({ kind: 'info', text: '' });
  const [busy, setBusy] = useState(false);
  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const load = async () => {
    try {
      setUsers(await get('/users'));
    } catch (err) {
      setMessage({ kind: 'error', text: err.message });
    }
  };
  useEffect(() => {
    load();
  }, []);

  const create = async (event) => {
    event.preventDefault();
    setBusy(true);
    try {
      const user = await post('/users', form);
      setMessage({ kind: 'success', text: `${user.fullName} can now log in as ${user.role} with the temporary password.` });
      setForm(EMPTY);
      load();
    } catch (err) {
      setMessage({ kind: 'error', text: err.message });
    } finally {
      setBusy(false);
    }
  };

  const toggle = async (user) => {
    try {
      await patch(`/users/${user.id}/status`, { isActive: !user.isActive });
      load();
    } catch (err) {
      setMessage({ kind: 'error', text: err.message });
    }
  };

  return html`
    <div class="page-head"><div><h1>Staff accounts</h1><p class="muted">Create drivers and facility operators, or switch accounts off.</p></div></div>
    <${Notice} kind=${message.kind}>${message.text}<//>
    <form class="card stack" onSubmit=${create}>
      <h2>New staff account</h2>
      <div class="row">
        <div><label for="s-name">Full name</label><input id="s-name" required value=${form.fullName} onInput=${set('fullName')} /></div>
        <div><label for="s-email">Email</label><input id="s-email" type="email" required value=${form.email} onInput=${set('email')} /></div>
      </div>
      <div class="row">
        <div>
          <label for="s-role">Role</label>
          <select id="s-role" value=${form.role} onChange=${set('role')}>
            <option value="DRIVER">Collection vehicle driver</option>
            <option value="OPERATOR">Disposal facility operator</option>
          </select>
        </div>
        <div>
          <label for="s-pass">Temporary password <span class="hint">(8+ characters)</span></label>
          <input id="s-pass" required minlength="8" value=${form.temporaryPassword} onInput=${set('temporaryPassword')} />
        </div>
      </div>
      <div class="actions"><button type="submit" disabled=${busy}>Create account</button></div>
    </form>
    <section class="card">
      <h2>All accounts</h2>
      <table class="responsive">
        <thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th></th></tr></thead>
        <tbody>
          ${users.map(
            (u) => html`<tr key=${u.id}>
              <td data-label="Name">${u.fullName}</td>
              <td data-label="Email">${u.email}</td>
              <td data-label="Role"><${Badge}>${u.role}<//></td>
              <td data-label="Status">${u.isActive ? 'Active' : 'Deactivated'}</td>
              <td data-label="">
                ${u.role !== 'ADMIN' &&
                html`<button class=${'small ' + (u.isActive ? 'danger' : 'ghost')} onClick=${() => toggle(u)}>
                  ${u.isActive ? 'Deactivate' : 'Reactivate'}
                </button>`}
              </td>
            </tr>`,
          )}
        </tbody>
      </table>
    </section>
  `;
}
