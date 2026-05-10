import React from 'react'
import { formatDate, formatPrice } from '../utils/formatters'

export default function PredictionPanel({ predictions }) {
  if (!predictions.length) return null

  return (
    <div>
      <h2 style={{ marginTop: 0, marginBottom: '0.75rem' }}>Predicted Prices</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.95rem' }}>
        <thead>
          <tr style={{ background: '#1a1a2e', color: '#f0c040' }}>
            <th style={{ padding: '0.6rem 1rem', textAlign: 'left' }}>Date</th>
            <th style={{ padding: '0.6rem 1rem', textAlign: 'right' }}>Predicted Price</th>
          </tr>
        </thead>
        <tbody>
          {predictions.map((p, i) => (
            <tr key={p.date} style={{ background: i % 2 === 0 ? '#fdf9ee' : '#fff' }}>
              <td style={{ padding: '0.5rem 1rem' }}>{formatDate(p.date)}</td>
              <td style={{ padding: '0.5rem 1rem', textAlign: 'right', fontWeight: 600 }}>
                {formatPrice(p.predicted_price)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
