import { useState, useEffect } from 'react';
import StatusBadge from '../components/StatusBadge';
import { api } from '../services/api';

export default function OwnerDashboard() {
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      const response = await api.getOwnerRequests();
      setRequests(response.data);
    } catch (error) {
      console.error("Error fetching requests:", error);
    }
  };

  const handleDecision = async (id, decision) => {
    try {
      if (decision === 'APPROVED') {
        await api.approveRequest(id);
      } else {
        await api.rejectRequest(id);
      }
      fetchRequests();
    } catch (error) {
      alert("Failed to process decision.");
    }
  };

  return (
    <div>
      <h1 style={{ marginBottom: '1.5rem' }}>Owner Dashboard</h1>
      
      <div className="table-container">
        {requests.length === 0 ? (
           <p style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>No pending requests.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Customer</th>
                <th>Description</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {requests.map(req => (
                <tr key={req.id}>
                  <td>#{req.id}</td>
                  <td style={{ fontWeight: '500' }}>{req.customer_name}</td>
                  <td>{req.description}</td>
                  <td><StatusBadge status={req.status} /></td>
                  <td>
                    {req.status === 'PENDING' ? (
                      <div style={{ display: 'flex', gap: '0.5rem' }}>
                        <button onClick={() => handleDecision(req.id, 'APPROVED')} className="btn btn-sm btn-success">
                          Approve
                        </button>
                        <button onClick={() => handleDecision(req.id, 'REJECTED')} className="btn btn-sm btn-danger">
                          Reject
                        </button>
                      </div>
                    ) : (
                      <span style={{ color: 'var(--text-muted)', fontStyle: 'italic', fontSize: '0.85rem' }}>
                        Decision Made
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}