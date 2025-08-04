import React, { useEffect, useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/customers`)
      .then(res => res.json())
      .then(data => {
        setCustomers(data.customers || []);
        setFiltered(data.customers || []);
        setLoading(false);
      })
      .catch(err => {
        setError('Failed to load customers', err);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    const q = search.toLowerCase();
    const f = customers.filter(c =>
      c.first_name.toLowerCase().includes(q) ||
      c.last_name.toLowerCase().includes(q) ||
      c.email.toLowerCase().includes(q)
    );
    setFiltered(f);
  }, [search, customers]);

  if (loading) return <p>Loading customers...</p>;
  if (error) return <p className="text-red-600">{error}</p>;

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Customer List</h1>
      <input
        type="text"
        placeholder="Search by name or email"
        className="border p-2 mb-4 w-full"
        value={search}
        onChange={e => setSearch(e.target.value)}
      />
      <table className="w-full table-auto border-collapse border">
        <thead>
          <tr className="bg-gray-100">
            <th className="border p-2">Name</th>
            <th className="border p-2">Email</th>
            <th className="border p-2">Order Count</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(customer => (
            <tr key={customer.user_id}>
              <td className="border p-2">{customer.first_name} {customer.last_name}</td>
              <td className="border p-2">{customer.email}</td>
              <td className="border p-2">{customer.order_count ?? 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CustomerList;