import React, { useState, useEffect } from 'react'
import axios from 'axios'
import ReviewQueue from './ReviewQueue'

const API_BASE = 'http://127.0.0.1:8000/api'

export default function Dashboard() {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchRecords = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_BASE}/records/`)
      setRecords(response.data)
      setError(null)
    } catch (err) {
      console.error(err)
      setError("Failed to fetch emissions data. Is the backend running?")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchRecords()
  }, [])

  const handleUpdateRecord = async (id, payload) => {
    try {
      await axios.patch(`${API_BASE}/records/${id}/`, payload)
      fetchRecords() // Refresh
    } catch (err) {
      console.error(err)
      alert("Failed to update record")
    }
  }

  return (
    <div>
      <h1 className="page-title">Analyst Dashboard</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
        Review and approve incoming emissions data before finalizing for audit.
      </p>

      {error && (
        <div style={{ padding: '16px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--danger)', borderRadius: '8px', marginBottom: '24px', color: 'var(--danger)' }}>
          {error}
        </div>
      )}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px' }}>Loading records...</div>
      ) : (
        <ReviewQueue records={records} onUpdate={handleUpdateRecord} />
      )}
    </div>
  )
}
