import React, { useState, useEffect } from 'react';
import './index.css';

function App() {
  const [user, setUser] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [tasks, setTasks] = useState([]);
  const [stateData, setStateData] = useState(null);
  const [activeTab, setActiveTab] = useState('dashboard');

  useEffect(() => {
    // Globally poll state every 2s
    fetchState();
    const stateInterval = setInterval(fetchState, 2000);
    
    // Fetch tasks if user is logged in
    if (user) {
      fetchTasks();
      const tasksInterval = setInterval(fetchTasks, 5000);
      return () => {
        clearInterval(stateInterval);
        clearInterval(tasksInterval);
      };
    }
    return () => clearInterval(stateInterval);
  }, [user]);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (data.success) {
        setUser({ username: data.username, role: data.role });
        setError('');
        setActiveTab('dashboard');
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('System is temporarily unavailable. Please wait...');
    }
  };

  const fetchTasks = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/tasks');
      const data = await res.json();
      if (data.success) {
        setTasks(data.tasks);
        setError('');
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('System is temporarily unavailable. Please wait...');
    }
  };

  const fetchState = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/state');
      const json = await res.json();
      setStateData(json);
    } catch (err) {}
  };

  // Detect critical system failures
  const isSystemDown = stateData && stateData.state && (
    stateData.state.server_status !== 'Running' ||
    stateData.state.db_status !== 'Connected' ||
    stateData.state.auth_status !== 'Working'
  );

  if (isSystemDown) {
    return (
      <div style={{ height: '100vh', width: '100vw', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#0a0a0a', color: '#ff4444', fontFamily: 'monospace' }}>
        <h1 style={{ fontSize: '84px', margin: '0 0 10px 0', textShadow: '0 0 20px rgba(255,0,0,0.5)' }}>503</h1>
        <h2 style={{ fontSize: '28px', letterSpacing: '4px', margin: 0 }}>CRITICAL SYSTEM FAILURE</h2>
        <div style={{ marginTop: '30px', padding: '30px', border: '1px solid #ff4444', backgroundColor: 'rgba(255, 68, 68, 0.05)', borderRadius: '8px', width: '400px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}><span>SERVER API:</span> <strong>{stateData.state.server_status}</strong></div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}><span>DATABASE:</span> <strong>{stateData.state.db_status}</strong></div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}><span>AUTH:</span> <strong>{stateData.state.auth_status}</strong></div>
        </div>
        <p style={{ marginTop: '50px', color: '#888', animation: 'pulse 2s infinite' }}>Stand by. OmniFix active...</p>
        <style>{`@keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }`}</style>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="login-container">
        <div className="login-card">
          <h2 className="login-title">OmniFix Enterprise Portal</h2>
          <p className="login-subtitle">Sign in to your account</p>
          
          {error && <div className="error-message">{error}</div>}

          <form onSubmit={handleLogin}>
            <div className="input-group">
              <label className="input-label">Username</label>
              <input 
                type="text" 
                className="input-field" 
                value={username} 
                onChange={e => setUsername(e.target.value)} 
                placeholder="e.g., employee1, manager1, admin1"
                required 
              />
            </div>
            <div className="input-group">
              <label className="input-label">Password</label>
              <input 
                type="password" 
                className="input-field" 
                value={password} 
                onChange={e => setPassword(e.target.value)} 
                placeholder="password123"
                required 
              />
            </div>
            <button type="submit" className="btn-primary">Sign In to Dashboard</button>
          </form>
        </div>
      </div>
    );
  }

  // Filter tasks based on role
  const myTasks = tasks.filter(t => t.assigned_to === user.username);
  const allTasks = tasks;
  
  const displayTasks = (user.role === 'Admin' || user.role === 'Manager') ? allTasks : myTasks;
  const pendingCount = displayTasks.filter(t => t.status === 'Pending').length;
  const completedCount = displayTasks.filter(t => t.status === 'Completed').length;

  return (
    <div className="app-container">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-header">
          <div className="brand">🚀 OmniFix</div>
        </div>
        
        <div className="nav-links">
          <div 
            className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </div>
          
          {(user.role === 'Manager' || user.role === 'Admin') && (
            <div 
              className={`nav-item ${activeTab === 'team' ? 'active' : ''}`}
              onClick={() => setActiveTab('team')}
            >
              Team Tasks
            </div>
          )}

          {user.role === 'Admin' && (
            <div 
              className={`nav-item ${activeTab === 'system' ? 'active' : ''}`}
              onClick={() => setActiveTab('system')}
            >
              System Health
            </div>
          )}
        </div>

        <div className="user-profile">
          <div className="avatar">
            {user.username.charAt(0).toUpperCase()}
          </div>
          <div className="user-info">
            <div className="user-name">{user.username}</div>
            <div className="user-role">{user.role}</div>
          </div>
          <button className="btn-logout" onClick={() => setUser(null)}>
            ⎋
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <div className="topbar">
          <div className="page-title">
            {activeTab === 'dashboard' && 'Dashboard'}
            {activeTab === 'team' && 'Team Tasks Overview'}
            {activeTab === 'system' && 'System Health Monitoring'}
          </div>
        </div>
        
        <div className="dashboard-content">
          {error && <div className="error-message">{error}</div>}

          {/* Stats Cards */}
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-label">Total Assigned Tasks</span>
              <span className="stat-value">{displayTasks.length}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Pending Reviews</span>
              <span className="stat-value" style={{ color: 'var(--warning)' }}>{pendingCount}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Completed Tasks</span>
              <span className="stat-value" style={{ color: 'var(--secondary)' }}>{completedCount}</span>
            </div>
          </div>

          {/* Tasks List */}
          {(activeTab === 'dashboard' || activeTab === 'team') && (
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">
                  {user.role === 'Admin' || user.role === 'Manager' ? 'All Organization Tasks' : 'My Pending Tasks'}
                </h3>
              </div>
              <ul className="task-list">
                {displayTasks.map(t => (
                  <li key={t.id} className="task-item">
                    <div className="task-info">
                      <span className="task-title">{t.title}</span>
                      <span className="task-meta">Assigned to: {t.assigned_to} • ID: #{t.id}</span>
                    </div>
                    <div>
                      <span className={`badge badge-${t.status.toLowerCase()}`}>
                        {t.status}
                      </span>
                    </div>
                  </li>
                ))}
                {displayTasks.length === 0 && (
                  <li className="task-item">
                    <div className="task-info">
                      <span className="task-title" style={{ color: 'var(--text-muted)' }}>No tasks found.</span>
                    </div>
                  </li>
                )}
              </ul>
            </div>
          )}

          {/* System Health Tab for Admin */}
          {activeTab === 'system' && stateData && stateData.state && (
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Global Services Status</h3>
              </div>
              <ul className="task-list">
                <li className="task-item">
                  <div className="task-info">
                    <span className="task-title">Core Backend Server</span>
                    <span className="task-meta">Main API processing instance</span>
                  </div>
                  <div>
                    <span className={`badge ${stateData.state.server_status === 'Running' ? 'badge-completed' : 'badge-pending'}`}>
                      {stateData.state.server_status}
                    </span>
                  </div>
                </li>
                <li className="task-item">
                  <div className="task-info">
                    <span className="task-title">Database Connection</span>
                    <span className="task-meta">PostgreSQL Cluster</span>
                  </div>
                  <div>
                    <span className={`badge ${stateData.state.db_status === 'Connected' ? 'badge-completed' : 'badge-pending'}`}>
                      {stateData.state.db_status}
                    </span>
                  </div>
                </li>
                <li className="task-item">
                  <div className="task-info">
                    <span className="task-title">Authentication Service</span>
                    <span className="task-meta">OAuth2.0 / JWT Gateway</span>
                  </div>
                  <div>
                    <span className={`badge ${stateData.state.auth_status === 'Working' ? 'badge-completed' : 'badge-pending'}`}>
                      {stateData.state.auth_status}
                    </span>
                  </div>
                </li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
