import { html } from '../lib.js';
import { getUser } from '../session.js';

export default function Home() {
  const user = getUser();
  return html`
    <section class="hero">
      <h1>Cleaner streets, planned smarter.</h1>
      <p>
        Request a waste pickup, follow it from approval to collection, and let the city plan
        the shortest safe routes for its vehicles.
      </p>
      ${user
        ? html`<p class="muted">Signed in as <strong>${user.fullName}</strong>. Pick a page from the menu.</p>`
        : html`<p><a class="button" href="#/login">Log in</a> <a class="button ghost" href="#/register">Create an account</a></p>`}
    </section>
  `;
}
