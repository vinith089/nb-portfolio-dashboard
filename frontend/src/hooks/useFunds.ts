/**
 * Custom hooks for fund data fetching
 */
'use client'

import { useState, useEffect } from 'react'
import { api, Fund, FundPerformanceResponse, PeerComparisonResponse, Holding } from '@/lib/api'

export function useFunds() {
  const [funds, setFunds] = useState<Fund[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchFunds() {
      try {
        setLoading(true)
        const data = await api.getFunds()
        setFunds(data)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch funds')
      } finally {
        setLoading(false)
      }
    }

    fetchFunds()
  }, [])

  return { funds, loading, error, refetch: () => window.location.reload() }
}

export function useFund(fundId: number) {
  const [fund, setFund] = useState<Fund | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!fundId) return

    async function fetchFund() {
      try {
        setLoading(true)
        const data = await api.getFund(fundId)
        setFund(data)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch fund')
      } finally {
        setLoading(false)
      }
    }

    fetchFund()
  }, [fundId])

  return { fund, loading, error }
}

export function useFundPerformance(fundId: number, days: number = 30) {
  const [performance, setPerformance] = useState<FundPerformanceResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!fundId) return

    async function fetchPerformance() {
      try {
        setLoading(true)
        const data = await api.getFundPerformance(fundId, days)
        setPerformance(data)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch performance')
      } finally {
        setLoading(false)
      }
    }

    fetchPerformance()
  }, [fundId, days])

  return { performance, loading, error }
}

export function useFundPeers(fundId: number) {
  const [peers, setPeers] = useState<PeerComparisonResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!fundId) return

    async function fetchPeers() {
      try {
        setLoading(true)
        const data = await api.getFundPeers(fundId)
        setPeers(data)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch peers')
      } finally {
        setLoading(false)
      }
    }

    fetchPeers()
  }, [fundId])

  return { peers, loading, error }
}

export function useFundHoldings(fundId: number) {
  const [holdings, setHoldings] = useState<Holding[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!fundId) return

    async function fetchHoldings() {
      try {
        setLoading(true)
        const data = await api.getHoldings(fundId)
        setHoldings(data)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch holdings')
      } finally {
        setLoading(false)
      }
    }

    fetchHoldings()
  }, [fundId])

  return { holdings, loading, error }
}