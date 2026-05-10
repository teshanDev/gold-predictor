import axios from 'axios'

const client = axios.create({ baseURL: (import.meta.env.VITE_API_URL || 'http://localhost:8000') + '/api' })

export const getCurrentPrice = () =>
  client.get('/gold/current-price').then(r => r.data)

export const getPredictions = (days = 7) =>
  client.get('/gold/predict', { params: { days } }).then(r => r.data)
