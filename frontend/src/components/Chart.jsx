import React from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { formatDate, formatPrice } from '../utils/formatters'

export default function Chart({ predictions }) {
  if (!predictions.length) return null

  const data = predictions.map(p => ({
    date: formatDate(p.date),
    price: p.predicted_price,
  }))

  return (
    <ResponsiveContainer width="100%" height={320}>
      <LineChart data={data} margin={{ top: 10, right: 20, left: 10, bottom: 10 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
        <XAxis dataKey="date" tick={{ fontSize: 12 }} />
        <YAxis
          domain={['auto', 'auto']}
          tickFormatter={v => `$${v.toLocaleString()}`}
          tick={{ fontSize: 12 }}
          width={85}
        />
        <Tooltip formatter={v => [formatPrice(v), 'Predicted Price']} />
        <Line
          type="monotone"
          dataKey="price"
          stroke="#f0c040"
          strokeWidth={2}
          dot={{ r: 3, fill: '#f0c040' }}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
