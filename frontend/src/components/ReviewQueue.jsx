import React, { useState } from 'react'

export default function ReviewQueue({ records, onUpdate }) {
  const [selectedRecord, setSelectedRecord] = useState(null)
  const [editValue, setEditValue] = useState('')

  const openModal = (record) => {
    setSelectedRecord(record)
    setEditValue(record.normalized_value || '')
  }

  const closeModal = () => {
    setSelectedRecord(null)
  }

  const handleApprove = (id) => {
    onUpdate(id, { status: 'APPROVED' })
    closeModal()
  }

  const handleLock = (id) => {
    if (window.confirm("Are you sure? This will lock the record for auditing and it cannot be changed again.")) {
      onUpdate(id, { status: 'LOCKED' })
      closeModal()
    }
  }

  const handleSaveEdit = (id) => {
    const val = parseFloat(editValue)
    if (isNaN(val)) {
      alert("Invalid numeric value")
      return
    }
    onUpdate(id, { normalized_value: val, status: 'PENDING' })
    closeModal()
  }

  const renderStatus = (status) => {
    const s = status.toLowerCase()
    return <span className={`status-badge status-${s}`}>{status}</span>
  }

  return (
    <div className="glass-panel data-table-wrapper">
      <table className="data-table">
        <thead>
          <tr>
            <th>Status</th>
            <th>Source</th>
            <th>Tenant</th>
            <th>Scope</th>
            <th>Description</th>
            <th>Emissions (kg CO2e)</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {records.map(r => {
            const isError = r.status === 'REJECTED'
            const isWarning = r.status === 'PENDING' && r.normalized_value > 1000 // Mock anomaly detection
            const rowClass = isError ? 'table-row-error' : (isWarning ? 'table-row-warning' : '')
            
            return (
              <tr key={r.id} className={rowClass}>
                <td>{renderStatus(r.status)}</td>
                <td><span style={{fontWeight: 500}}>{r.source_system}</span></td>
                <td>{r.tenant_name}</td>
                <td>{r.scope}</td>
                <td>{r.description}</td>
                <td>
                  <span style={{ fontFamily: 'monospace', fontSize: '1rem', color: isError ? 'var(--danger)' : 'inherit' }}>
                    {r.normalized_value !== null ? r.normalized_value.toLocaleString() : 'N/A'}
                  </span>
                </td>
                <td>
                  <button 
                    className="btn btn-outline" 
                    style={{ padding: '4px 8px', fontSize: '0.8rem' }}
                    onClick={() => openModal(r)}
                  >
                    Review
                  </button>
                </td>
              </tr>
            )
          })}
          {records.length === 0 && (
            <tr>
              <td colSpan="7" style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
                No records found.
              </td>
            </tr>
          )}
        </tbody>
      </table>

      {selectedRecord && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content glass-panel" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3 className="modal-title">Review Record</h3>
              <button className="modal-close" onClick={closeModal}>✕</button>
            </div>
            
            <div style={{ marginBottom: '24px' }}>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '8px' }}>
                <strong>Source:</strong> {selectedRecord.source_system} | <strong>Tenant:</strong> {selectedRecord.tenant_name}
              </p>
              <div style={{ padding: '12px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px', fontSize: '0.85rem', fontFamily: 'monospace', wordBreak: 'break-all' }}>
                {JSON.stringify(selectedRecord.raw_data)}
              </div>
            </div>

            {selectedRecord.status !== 'LOCKED' ? (
              <div className="form-group">
                <label className="form-label">Calculated Emissions (kg CO2e)</label>
                <input 
                  type="number" 
                  className="form-control" 
                  value={editValue} 
                  onChange={e => setEditValue(e.target.value)} 
                />
              </div>
            ) : (
              <div style={{ padding: '12px', background: 'var(--primary-color)', color: 'white', borderRadius: '8px', marginBottom: '20px', textAlign: 'center' }}>
                🔒 This record is locked for auditing and cannot be edited.
              </div>
            )}

            <div style={{ display: 'flex', gap: '12px', marginTop: '32px' }}>
              {selectedRecord.status !== 'LOCKED' && (
                <>
                  <button className="btn btn-outline" onClick={() => handleSaveEdit(selectedRecord.id)}>
                    Save Edit
                  </button>
                  <button className="btn btn-success" onClick={() => handleApprove(selectedRecord.id)}>
                    Approve
                  </button>
                  <button className="btn btn-primary" onClick={() => handleLock(selectedRecord.id)}>
                    Lock for Audit
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
