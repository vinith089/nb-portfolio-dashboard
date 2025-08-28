'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { FundPerformanceData } from '@/lib/api'

interface PerformanceChartProps {
  data: FundPerformanceData[]
  fundName: string
}

export function PerformanceChart({ data }: PerformanceChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">No performance data available</p>
      </div>
    )
  }

  const chartData = data.map((item) => ({
    date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    navPrice: Number(item.nav_price) || 0,
    totalReturn: item.total_return != null ? Number(item.total_return) : 0,
    dailyReturn: item.daily_return != null ? Number(item.daily_return) : 0,
  }))

  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={chartData}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
          <XAxis 
            dataKey="date" 
            fontSize={12}
            tick={{ fill: 'currentColor' }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis 
            yAxisId="return"
            fontSize={12}
            tick={{ fill: 'currentColor' }}
            axisLine={false}
            tickLine={false}
            label={{ value: 'Return (%)', angle: -90, position: 'insideLeft' }}
          />
          <YAxis 
            yAxisId="nav"
            orientation="right"
            fontSize={12}
            tick={{ fill: 'currentColor' }}
            axisLine={false}
            tickLine={false}
            label={{ value: 'NAV Price ($)', angle: 90, position: 'insideRight' }}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            }}
            labelStyle={{ color: '#374151' }}
          />
          <Line 
            type="monotone" 
            dataKey="navPrice" 
            stroke="#2563eb" 
            strokeWidth={2}
            dot={false}
            name="NAV Price ($)"
            yAxisId="nav"
          />
          <Line 
            type="monotone" 
            dataKey="totalReturn" 
            stroke="#059669" 
            strokeWidth={2}
            dot={false}
            name="Total Return (%)"
            yAxisId="return"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}