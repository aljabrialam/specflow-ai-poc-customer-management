import { useEffect, useMemo, useState } from 'react';
import './App.css';

type Customer = {
  id: number;
  name: string;
  email: string;
  phone: string;
  company: string;
};

type CustomerForm = {
  name: string;
  email: string;
  phone: string;
  company: string;
};

const emptyForm: CustomerForm = {
  name: '',
  email: '',
  phone: '',
  company: '',
};

function App() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [form, setForm] = useState<CustomerForm>(emptyForm);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const apiBaseUrl = useMemo(() => import.meta.env.VITE_API_URL || '', []);

  const loadCustomers = async () => {
    const response = await fetch(`${apiBaseUrl}/api/customers`);
    const data = await response.json();
    setCustomers(data);
  };

  useEffect(() => {
    loadCustomers().catch(() => {
      setError('Unable to reach the API service.');
    });
  }, [apiBaseUrl]);

  const submitCustomer = async (event: React.FormEvent) => {
    event.preventDefault();
    setError('');
    setMessage('');

    const request = editingId === null
      ? fetch(`${apiBaseUrl}/api/customers`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(form),
        })
      : fetch(`${apiBaseUrl}/api/customers/${editingId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(form),
        });

    const response = await request;
    const body = await response.json().catch(() => ({}));

    if (!response.ok) {
      setError(body.detail || 'Unable to save customer.');
      return;
    }

    setForm(emptyForm);
    setEditingId(null);
    setMessage(editingId === null ? 'Customer created.' : 'Customer updated.');
    await loadCustomers();
  };

  const startEdit = (customer: Customer) => {
    setEditingId(customer.id);
    setForm({
      name: customer.name,
      email: customer.email,
      phone: customer.phone,
      company: customer.company,
    });
    setMessage('');
    setError('');
  };

  const deleteCustomer = async (customerId: number) => {
    const response = await fetch(`${apiBaseUrl}/api/customers/${customerId}`, { method: 'DELETE' });
    if (!response.ok) {
      setError('Unable to delete customer.');
      return;
    }
    setMessage('Customer deleted.');
    await loadCustomers();
  };

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Customer Management Portal</p>
          <h1>Maintain your customer records with confidence.</h1>
          <p>Create, update, and remove customers from one simple experience.</p>
        </div>
      </header>

      <main className="content-grid">
        <section className="card">
          <h2>{editingId === null ? 'Create customer' : 'Edit customer'}</h2>
          <form onSubmit={submitCustomer} className="customer-form">
            <label>
              Name
              <input value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} required />
            </label>
            <label>
              Email
              <input type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} required />
            </label>
            <label>
              Phone
              <input value={form.phone} onChange={(event) => setForm({ ...form, phone: event.target.value })} required />
            </label>
            <label>
              Company
              <input value={form.company} onChange={(event) => setForm({ ...form, company: event.target.value })} required />
            </label>
            <div className="actions">
              <button type="submit">{editingId === null ? 'Create customer' : 'Save changes'}</button>
              {editingId !== null ? (
                <button type="button" className="secondary" onClick={() => { setEditingId(null); setForm(emptyForm); }}>
                  Cancel
                </button>
              ) : null}
            </div>
          </form>
          {message ? <p className="message">{message}</p> : null}
          {error ? <p className="error">{error}</p> : null}
        </section>

        <section className="card">
          <h2>Customers</h2>
          <div className="customer-list">
            {customers.map((customer) => (
              <article key={customer.id} className="customer-row">
                <div>
                  <strong>{customer.name}</strong>
                  <p>{customer.email}</p>
                  <p>{customer.phone}</p>
                  <p>{customer.company}</p>
                </div>
                <div className="row-actions">
                  <button type="button" className="secondary" onClick={() => startEdit(customer)}>Edit</button>
                  <button type="button" onClick={() => deleteCustomer(customer.id)}>Delete</button>
                </div>
              </article>
            ))}
            {customers.length === 0 ? <p>No customers yet.</p> : null}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
