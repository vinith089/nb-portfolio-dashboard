'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { PeerComparisonData } from '@/lib/api'

interface PeerComparisonChartProps {
  peers: PeerComparisonData[]
  currentFund: {
    name: string
    performance: number | null
  }
}

export function PeerComparisonChart({ peers, currentFund }: PeerComparisonChartProps) {
  if (!peers || peers.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">No peer comparison data available</p>
      </div>
    )
  }

  const chartData = [
    {
      name: currentFund.name.length > 20 ? currentFund.name.substring(0, 17) + '...' : currentFund.name,
      performance: currentFund.performance != null ? Number(currentFund.performance) : 0,
      isCurrentFund: true,
    },
    ...peers.slice(0, 4).map((peer) => ({
      name: peer.fund_name.length > 20 ? peer.fund_name.substring(0, 17) + '...' : peer.fund_name,
      performance: peer.total_return != null ? Number(peer.total_return) : 0,
      isCurrentFund: false,
    }))
  ]

  const CustomTooltip = ({ active, payload, label }: { active?: boolean; payload?: any[]; label?: string }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900">{label}</p>
          <p className="text-sm text-gray-600">
            Performance: <span className={`font-medium ${(data.performance || 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {data.performance != null ? (
                `${data.performance >= 0 ? '+' : ''}${Number(data.performance).toFixed(2)}%`
              ) : (
                'N/A'
              )}
            </span>
          </p>
          {data.isCurrentFund && (
            <p className="text-xs text-blue-600 mt-1">Current Fund</p>
          )}
        </div>
      )
    }
    return null
  }

  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 60,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
          <XAxis 
            dataKey="name" 
            fontSize={12}
            tick={{ fill: 'currentColor' }}
            axisLine={false}
            tickLine={false}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis 
            fontSize={12}
            tick={{ fill: 'currentColor' }}
            axisLine={false}
            tickLine={false}
            label={{ value: 'Performance (%)', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar 
            dataKey="performance" 
            fill="#6b7280"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}