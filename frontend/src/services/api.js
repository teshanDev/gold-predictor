import axios from 'axios'

const client = axios.create({ baseURL: '/api' })

export const getCurrentPrice = () =>
  client.get('/gold/current-price').then(r => r.data)

export const getPredictions = (days = 7) =>
  client.get('/gold/predict', { params: { days } }).then(r => r.data)
