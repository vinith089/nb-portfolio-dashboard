const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface Fund {
  id: number
  name: string
  strategy: string
  inception_date: string
  total_aum: string
  manager_name: string | null
  expense_ratio: string
  description: string | null
  created_at: string
  updated_at: string
  holdings_count: number
  current_value: string | null
  total_return_percent: number | null
  daily_return_percent: number | null
  unrealized_gain_loss: string
  unrealized_gain_loss_percent: string
}

export interface Holding {
  id: number
  fund_id: number
  ticker: string
  company_name: string | null
  shares: string
  purchase_price: string
  purchase_date: string
  sector: string | null
  market_cap: number | null
  created_at: string
  updated_at: string
  cost_basis: string
  current_price: string | null
  current_value: string | null
  unrealized_gain_loss: string | null
  unrealized_gain_loss_percent: string | null
  weight_in_fund: string | null
}

export interface FundPerformanceData {
  date: string
  nav_price: string
  total_return: number | null
  daily_return: number | null
  assets_under_management: string | null
}

export interface FundPerformanceResponse {
  fund_id: number
  fund_name: string
  performance_data: FundPerformanceData[]
  period_days: number
}

export interface PeerComparisonData {
  fund_id: number
  fund_name: string
  benchmark_category: string
  total_aum: string | null
  expense_ratio: string | null
  total_return: number | null
}

export interface PeerComparisonResponse {
  fund_id: number
  fund_name: string
  fund_strategy: string
  fund_performance: number | null
  peers: PeerComparisonData[]
}

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = 'ApiError'
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorText = await response.text()
    throw new ApiError(response.status, errorText || response.statusText)
  }
  
  const contentType = response.headers.get('content-type')
  if (contentType && contentType.includes('application/json')) {
    return response.json()
  }
  
  return response.text() as T
}

export const api = {
  // Fund endpoints
  async getFunds(): Promise<Fund[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/funds/`)
    return handleResponse<Fund[]>(response)
  },

  async getFund(fundId: number): Promise<Fund> {
    const response = await fetch(`${API_BASE_URL}/api/v1/funds/${fundId}`)
    return handleResponse<Fund>(response)
  },

  async getFundPerformance(fundId: number, days: number = 30): Promise<FundPerformanceResponse> {
    const response = await fetch(`${API_BASE_URL}/api/v1/funds/${fundId}/performance?days=${days}`)
    return handleResponse<FundPerformanceResponse>(response)
  },

  async getFundPeers(fundId: number): Promise<PeerComparisonResponse> {
    const response = await fetch(`${API_BASE_URL}/api/v1/funds/${fundId}/peers`)
    return handleResponse<PeerComparisonResponse>(response)
  },

  async getFundStats(fundId: number): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/v1/funds/${fundId}/stats`)
    return handleResponse<any>(response)
  },

  // Holdings endpoints
  async getHoldings(fundId?: number): Promise<Holding[]> {
    const url = fundId 
      ? `${API_BASE_URL}/api/v1/holdings/?fund_id=${fundId}`
      : `${API_BASE_URL}/api/v1/holdings/`
    const response = await fetch(url)
    return handleResponse<Holding[]>(response)
  },

  async getFundHoldingsSummary(fundId: number): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/v1/holdings/fund/${fundId}/summary`)
    return handleResponse<any>(response)
  },

  async getFundTopHoldings(fundId: number, limit: number = 10): Promise<Holding[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/holdings/fund/${fundId}/top?limit=${limit}`)
    return handleResponse<Holding[]>(response)
  },
}

// Utility functions for formatting
export function formatCurrency(amount: number | string): string {
  const num = typeof amount === 'string' ? parseFloat(amount) : amount
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(num)
}

export function formatPercent(percent: number | string | null): string {
  if (percent === null || percent === undefined) return 'N/A'
  const num = typeof percent === 'string' ? parseFloat(percent) : percent
  return `${num >= 0 ? '+' : ''}${num.toFixed(2)}%`
}

export function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}