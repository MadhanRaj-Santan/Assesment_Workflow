import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import CustomerDashboard from './pages/CustomerDashboard';
import OwnerDashboard from './pages/OwnerDashboard';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <nav className="navbar">
          <div className="navbar-brand">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '10px' }}>
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            <h2>ApprovalFlow</h2>
          </div>
          <div className="nav-links">
            <NavLink to="/" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
              Customer Dashboard
            </NavLink>
            <NavLink to="/owner" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
              Owner Dashboard
            </NavLink>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<CustomerDashboard />} />
            <Route path="/owner" element={<OwnerDashboard />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;