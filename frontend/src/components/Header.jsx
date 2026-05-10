import React from 'react'
import { formatPrice } from '../utils/formatters'

export default function Header({ currentPrice }) {
  return (
    <header style={{
      background: '#1a1a2e',
      color: '#f0c040',
      padding: '1rem 2rem',
      display: 'flex',
      alignItems: 'center',
      gap: '2rem',
    }}>
      <h1 style={{ margin: 0, fontSize: '1.4rem' }}>Gold Price Predictor</h1>
      {currentPrice != null && (
        <span style={{ fontSize: '1.1rem', color: '#fff' }}>
          Live: <strong style={{ color: '#f0c040' }}>{formatPrice(currentPrice)}</strong>
        </span>
      )}
    </header>
  )
}
