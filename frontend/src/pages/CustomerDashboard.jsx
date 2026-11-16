import { useState, useEffect } from 'react';
import FileUpload from '../components/FileUpload';
import StatusBadge from '../components/StatusBadge';
import { api } from '../services/api';

export default function CustomerDashboard() {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState(null);
  const [requests, setRequests] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false); // Interaction state

  useEffect(() => {
    fetchRequests();
    const interval = setInterval(fetchRequests, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchRequests = async () => {
    try {
      const response = await api.getCustomerRequests();
      setRequests(response.data);
    } catch (error) {
      console.error("Error fetching requests:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please attach a file.");

    setIsSubmitting(true);
    const formData = new FormData();
    formData.append('customer_name', name);
    formData.append('description', description);
    formData.append('file', file);

    try {
      await api.submitRequest(formData);
      setName('');
      setDescription('');
      setFile(null);
      fetchRequests();
    } catch (error) {
      alert('Failed to submit request.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div>
      <h1 style={{ marginBottom: '1.5rem' }}>Customer Dashboard</h1>
      
      <div className="card">
        <h2 style={{ marginBottom: '1rem' }}>Submit a Request</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Name</label>
            <input type="text" value={name} onChange={(e) => setName(e.target.value)} required placeholder="Enter your full name" />
          </div>
          <div className="form-group">
            <label>Description</label>
            <textarea value={description} onChange={(e) => setDescription(e.target.value)} required placeholder="Briefly describe your request..." rows="3" />
          </div>
          
          <div className="form-group">
             <FileUpload onFileSelect={setFile} />
          </div>

          <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
            {isSubmitting ? 'Submitting...' : 'Submit Request'}
          </button>
        </form>
      </div>

      <h2 style={{ marginBottom: '1rem' }}>My Requests</h2>
      <div className="table-container">
        {requests.length === 0 ? (
          <p style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>No requests submitted yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Description</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {requests.map(req => (
                <tr key={req.id}>
                  <td>#{req.id}</td>
                  <td>{req.description}</td>
                  <td><StatusBadge status={req.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}