import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [items, setItems] = useState([]);
  const [stats, setStats] = useState({ total: 0, applied: 0, interview: 0, offer: 0, rejected: 0 });
  const [error, setError] = useState("");
  const empty = { company: "", position: "", location: "", status: "Applied", job_url: "", applied_date: "", notes: "" };
  const [form, setForm] = useState(empty);

  const authHeaders = { Authorization: `Bearer ${token}` };

  async function loadData() {
    if (!token) return;
    const [apps, dash] = await Promise.all([
      fetch(`${API}/api/applications`, { headers: authHeaders }),
      fetch(`${API}/api/dashboard`, { headers: authHeaders })
    ]);
    if (apps.status === 401) return logout();
    setItems(await apps.json());
    setStats(await dash.json());
  }

  useEffect(() => { loadData(); }, [token]);

  async function submitAuth(e) {
    e.preventDefault();
    setError("");
    if (mode === "register") {
      const r = await fetch(`${API}/auth/register`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      if (!r.ok) return setError((await r.json()).detail || "Registration failed");
    }
    const body = new URLSearchParams({ username: email, password });
    const r = await fetch(`${API}/auth/login`, {
      method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body
    });
    if (!r.ok) return setError("Invalid email or password");
    const data = await r.json();
    localStorage.setItem("token", data.access_token);
    setToken(data.access_token);
  }

  async function addApplication(e) {
    e.preventDefault();
    const payload = { ...form, applied_date: form.applied_date || null };
    const r = await fetch(`${API}/api/applications`, {
      method: "POST",
      headers: { ...authHeaders, "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (r.ok) {
      setForm(empty);
      loadData();
    }
  }

  async function remove(id) {
    await fetch(`${API}/api/applications/${id}`, { method: "DELETE", headers: authHeaders });
    loadData();
  }

  function logout() {
    localStorage.removeItem("token");
    setToken("");
    setItems([]);
  }

  if (!token) return (
    <main className="auth-shell">
      <section className="card auth-card">
        <h1>Job Application Tracker</h1>
        <p>Track applications, interviews, offers, and follow-ups.</p>
        <form onSubmit={submitAuth}>
          <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
          <input type="password" placeholder="Password (6+ characters)" value={password} onChange={e => setPassword(e.target.value)} required />
          {error && <p className="error">{error}</p>}
          <button>{mode === "login" ? "Sign in" : "Create account"}</button>
        </form>
        <button className="link" onClick={() => setMode(mode === "login" ? "register" : "login")}>
          {mode === "login" ? "Create an account" : "Already have an account?"}
        </button>
      </section>
    </main>
  );

  return (
    <main className="container">
      <header>
        <div><h1>Job Application Tracker</h1><p>Full-stack portfolio project</p></div>
        <button className="secondary" onClick={logout}>Log out</button>
      </header>

      <section className="stats">
        {Object.entries(stats).map(([k,v]) => <div className="card stat" key={k}><strong>{v}</strong><span>{k}</span></div>)}
      </section>

      <section className="grid">
        <div className="card">
          <h2>Add application</h2>
          <form onSubmit={addApplication}>
            <input placeholder="Company" value={form.company} onChange={e=>setForm({...form, company:e.target.value})} required />
            <input placeholder="Position" value={form.position} onChange={e=>setForm({...form, position:e.target.value})} required />
            <input placeholder="Location" value={form.location} onChange={e=>setForm({...form, location:e.target.value})} />
            <select value={form.status} onChange={e=>setForm({...form, status:e.target.value})}>
              <option>Applied</option><option>Interview</option><option>Offer</option><option>Rejected</option>
            </select>
            <input type="date" value={form.applied_date} onChange={e=>setForm({...form, applied_date:e.target.value})} />
            <input placeholder="Job URL" value={form.job_url} onChange={e=>setForm({...form, job_url:e.target.value})} />
            <textarea placeholder="Notes" value={form.notes} onChange={e=>setForm({...form, notes:e.target.value})} />
            <button>Add application</button>
          </form>
        </div>

        <div className="card">
          <h2>Your applications</h2>
          <div className="list">
            {items.length === 0 && <p>No applications yet.</p>}
            {items.map(item => (
              <article className="job" key={item.id}>
                <div>
                  <h3>{item.position}</h3>
                  <p>{item.company} · {item.location || "Location not set"}</p>
                  <span className="badge">{item.status}</span>
                </div>
                <button className="danger" onClick={()=>remove(item.id)}>Delete</button>
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
