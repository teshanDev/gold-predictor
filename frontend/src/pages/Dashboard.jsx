import React, { useState } from 'react'
import Header from '../components/Header'
import Chart from '../components/Chart'
import PredictionPanel from '../components/PredictionPanel'
import { useGoldPrice } from '../hooks/useGoldPrice'

const card = {
  background: '#fff',
  borderRadius: 8,
  padding: '1.5rem',
  boxShadow: '0 1px 4px rgba(0,0,0,0.1)',
}

export default function Dashboard() {
  const [days, setDays] = useState(7)
  const { currentPrice, predictions, loading, error } = useGoldPrice(days)

  return (
    <div style={{ fontFamily: 'sans-serif', minHeight: '100vh', background: '#f5f5f5' }}>
      <Header currentPrice={currentPrice} />
      <main style={{ maxWidth: 900, margin: '2rem auto', padding: '0 1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
          <label htmlFor="days" style={{ fontWeight: 600 }}>Forecast horizon:</label>
          <select
            id="days"
            value={days}
            onChange={e => setDays(Number(e.target.value))}
            style={{ padding: '0.4rem 0.8rem', borderRadius: 4, border: '1px solid #ccc' }}
          >
            {[3, 7, 14, 30].map(d => (
              <option key={d} value={d}>{d} days</option>
            ))}
          </select>
        </div>

        {loading && <p>Loading predictions…</p>}
        {error && <p style={{ color: '#c0392b' }}>Error: {error}</p>}

        {!loading && !error && (
          <div style={{ display: 'grid', gap: '2rem' }}>
            <div style={card}>
              <h2 style={{ marginTop: 0 }}>Price Forecast</h2>
              <Chart predictions={predictions} />
            </div>
            <div style={card}>
              <PredictionPanel predictions={predictions} />
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
