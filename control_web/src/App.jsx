import React, { useState, useEffect, useRef } from 'react';
import './index.css';

function App() {
  const [data, setData] = useState({ state: null, tickets: [], logs: [] });
  const [activeMode, setActiveMode] = useState('threat'); // 'threat' or 'aegis'
  const [selectedTicketId, setSelectedTicketId] = useState(null);
  const [chatLogs, setChatLogs] = useState([]);
  const [activeAgent, setActiveAgent] = useState('Dispatcher');
  
  const chatEndRef = useRef(null);

  // Poll for global state
  const fetchState = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/state');
      const json = await res.json();
      setData(json);
    } catch (err) {}
  };

  useEffect(() => {
    fetchState();
    const interval = setInterval(fetchState, 2000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Scroll to bottom of chat
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatLogs]);

  const triggerAttack = async (action, title) => {
    await fetch('http://127.0.0.1:5000/api/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action })
    });
    
    // Auto-create Aegis ticket
    await fetch('http://127.0.0.1:5000/api/ticket', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'Security Alert', description: `Detected anomaly: ${title}` })
    });
    
    fetchState();
    
    // Switch to Aegis to show it reacts
    setTimeout(() => {
      setActiveMode('aegis');
    }, 1500);
  };

  const startAegisResolution = (ticketId) => {
    setSelectedTicketId(ticketId);
    setChatLogs([]);
    const source = new EventSource(`http://127.0.0.1:5000/api/run_omnifix?ticket_id=${ticketId}`);
    
    source.onmessage = (event) => {
      const resp = JSON.parse(event.data);
      if (resp.type === 'chat') {
        setChatLogs(prev => [...prev, resp]);
        setActiveAgent(resp.sender);
      } else if (resp.type === 'system') {
        setChatLogs(prev => [...prev, { ...resp, system: true }]);
      }

      if (resp.done) {
        source.close();
        setActiveAgent('Verifier');
        setTimeout(fetchState, 1000);
      }
    };
  };

  const { state, tickets } = data;

  if (!state) return <div className="app-container">Connecting to Core Network...</div>;

  return (
    <>
      <nav className="top-nav">
        <div className="nav-brand">
          <span style={{color: activeMode === 'threat' ? 'var(--threat-primary)' : 'var(--aegis-primary)'}}>
            {activeMode === 'threat' ? '☠️ RED TEAM' : '🛡️ OMNIFIX'}
          </span>
        </div>
        <div className="nav-tabs">
          <button 
            className={`nav-tab threat ${activeMode === 'threat' ? 'active' : ''}`}
            onClick={() => setActiveMode('threat')}
          >
            Threat Simulator
          </button>
          <button 
            className={`nav-tab aegis ${activeMode === 'aegis' ? 'active' : ''}`}
            onClick={() => setActiveMode('aegis')}
          >
            OmniFix Defense Portal
          </button>
        </div>
      </nav>

      <div className="app-container">
        {activeMode === 'threat' ? (
          <div className="threat-grid">
            {/* Target Topology */}
            <div className="panel">
              <div className="panel-header">🎯 Target Topology Status</div>
              <div className="system-map">
                <div className="node">
                  <div style={{fontWeight: 'bold'}}>Core API Server</div>
                  <div className={`node-status ${state.server_status === 'Running' ? 'operational' : 'down'}`}>
                    {state.server_status === 'Running' ? 'ONLINE' : 'OFFLINE'}
                  </div>
                </div>
                <div className="node">
                  <div style={{fontWeight: 'bold'}}>Postgres Database Cluster</div>
                  <div className={`node-status ${state.db_status === 'Connected' ? 'operational' : 'down'}`}>
                    {state.db_status === 'Connected' ? 'ONLINE' : 'OFFLINE'}
                  </div>
                </div>
                <div className="node">
                  <div style={{fontWeight: 'bold'}}>Auth Gateway (OAuth)</div>
                  <div className={`node-status ${state.auth_status === 'Working' ? 'operational' : 'down'}`}>
                    {state.auth_status === 'Working' ? 'ONLINE' : 'OFFLINE'}
                  </div>
                </div>
              </div>
            </div>

            {/* Attack Vectors */}
            <div className="panel">
              <div className="panel-header">🔪 Available Attack Vectors</div>
              <div className="attack-card">
                <div className="attack-card-header">
                  <span className="attack-title">DDoS on API Server</span>
                  <span className="attack-badge">Critical</span>
                </div>
                <div className="attack-path">
                  POST /api/simulate HTTP/1.1<br/>
                  Action: Flood connections (server_down)
                </div>
                <button className="btn-attack" onClick={() => triggerAttack('server_down', 'API Server DDoS')}>LAUNCH ATTACK</button>
              </div>

              <div className="attack-card">
                <div className="attack-card-header">
                  <span className="attack-title">Database Injection Drop</span>
                  <span className="attack-badge">Critical</span>
                </div>
                <div className="attack-path">
                  sql_query: DROP TABLE users; -- (db_down)
                </div>
                <button className="btn-attack" onClick={() => triggerAttack('db_down', 'Database Connection Severed')}>INJECT SQL</button>
              </div>

              <div className="attack-card">
                <div className="attack-card-header">
                  <span className="attack-title">Auth Token Hijack</span>
                  <span className="attack-badge">High</span>
                </div>
                <div className="attack-path">
                  Exploiting missing signature validation (auth_fail)
                </div>
                <button className="btn-attack" onClick={() => triggerAttack('auth_fail', 'Auth Gateway Disconnected')}>BYPASS AUTH</button>
              </div>
            </div>
          </div>
        ) : (
          <div className="aegis-grid">
            {/* Ticket Sidebar */}
            <div className="panel">
              <div className="panel-header" style={{color: 'var(--aegis-primary)'}}>Incidents Console</div>
              <div className="ticket-list">
                {tickets.map(t => (
                  <div key={t.id} className={`ticket-card ${selectedTicketId === t.id ? 'selected' : ''}`} onClick={() => startAegisResolution(t.id)}>
                    <div className="ticket-header">
                      <span className="ticket-id">#{t.id}</span>
                      <span className={`ticket-status ${t.status.toLowerCase()}`}>{t.status}</span>
                    </div>
                    <div style={{fontSize: '14px', color: 'var(--text-muted)'}}>{t.desc || 'No description provided.'}</div>
                    {t.status !== 'Resolved' && (
                      <button style={{width: '100%', padding: '10px', marginTop: '10px', background: 'var(--aegis-primary)', color: 'black', fontWeight: 'bold', border: 'none', borderRadius: '4px', cursor: 'pointer'}}>ENGAGE OMNIFIX</button>
                    )}
                  </div>
                ))}
                {tickets.length === 0 && <div className="empty-state" style={{fontSize: '14px'}}>Scanning for anomalies... All clear.</div>}
              </div>
            </div>

            {/* Chat Flow */}
            <div className="panel chat-container">
              <div className="panel-header" style={{color: 'var(--aegis-primary)'}}>
                Multi-Agent Resolution Hub
              </div>
              
              {!selectedTicketId ? (
                <div className="empty-state">Select an incident to view Agent Chat logs.</div>
              ) : (
                <>
                  <div className="chat-history">
                    {chatLogs.map((log, idx) => (
                      log.system ? (
                        <div key={idx} className="system-msg">{log.log}</div>
                      ) : (
                        <div key={idx} className="chat-msg">
                          <div className="agent-avatar">{log.sender.substring(0, 1)}</div>
                          <div className="msg-content">
                            <div className="msg-sender">{log.sender} AI</div>
                            <div className="msg-text">{log.message}</div>
                          </div>
                        </div>
                      )
                    ))}
                    <div ref={chatEndRef} />
                  </div>

                  <div className="agents-status-bar">
                    <div className={`agent-indicator ${activeAgent === 'Dispatcher' ? 'active' : ''}`}>1. Dispatcher</div>
                    <div className={`agent-indicator ${activeAgent === 'Diagnostician' ? 'active' : ''}`}>2. Diagnostician</div>
                    <div className={`agent-indicator ${activeAgent === 'Remediation' ? 'active' : ''}`}>3. Remediation</div>
                    <div className={`agent-indicator ${activeAgent === 'Verifier' ? 'active' : ''}`}>4. Verifier</div>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export default App;
