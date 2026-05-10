import { useState, useEffect } from 'react'
import { getCurrentPrice, getPredictions } from '../services/api'

export function useGoldPrice(days = 7) {
  const [currentPrice, setCurrentPrice] = useState(null)
  const [predictions, setPredictions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    Promise.all([getCurrentPrice(), getPredictions(days)])
      .then(([priceData, predData]) => {
        setCurrentPrice(priceData.price)
        setPredictions(predData)
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [days])

  return { currentPrice, predictions, loading, error }
}
