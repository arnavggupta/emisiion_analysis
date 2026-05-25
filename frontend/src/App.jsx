import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './components/Dashboard'

function App() {
  return (
    <Router>
      <div className="app-container">
        <aside className="sidebar glass-panel" style={{ borderTopLeftRadius: 0, borderBottomLeftRadius: 0, borderRight: '1px solid rgba(255,255,255,0.1)' }}>
          <div style={{ marginBottom: '40px' }}>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--primary-color)' }}>BreatheSG</h2>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Enterprise Emissions</p>
          </div>
          
          <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <a href="#" className="btn btn-primary" style={{ justifyContent: 'flex-start' }}>
              <span className="icon">📊</span> Dashboard
            </a>
            <a href="#" className="btn btn-outline" style={{ justifyContent: 'flex-start', border: 'none' }}>
              <span className="icon">🏢</span> Tenants
            </a>
            <a href="#" className="btn btn-outline" style={{ justifyContent: 'flex-start', border: 'none' }}>
              <span className="icon">⚙️</span> Settings
            </a>
          </nav>
        </aside>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
