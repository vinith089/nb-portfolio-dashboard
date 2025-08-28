"use client";

import { use } from "react";
import Link from "next/link";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  ArrowLeftIcon,
  LoaderIcon,
  TrendingUpIcon,
  DollarSignIcon,
  FolderIcon,
  BarChart3Icon,
} from "lucide-react";
import {
  useFund,
  useFundHoldings,
  useFundPerformance,
  useFundPeers,
} from "@/hooks/useFunds";
import { formatCurrency, formatPercent, formatDate } from "@/lib/api";
import { PerformanceChart } from "@/components/charts/PerformanceChart";
import { PeerComparisonChart } from "@/components/charts/PeerComparisonChart";

interface FundDetailPageProps {
  params: Promise<{ id: string }>;
}

export default function FundDetailPage({ params }: FundDetailPageProps) {
  const { id } = use(params);
  const fundId = parseInt(id);

  const { fund, loading: fundLoading, error: fundError } = useFund(fundId);
  const { holdings, loading: holdingsLoading } = useFundHoldings(fundId);
  const { performance, loading: performanceLoading } = useFundPerformance(
    fundId,
    90
  );
  const { peers, loading: peersLoading } = useFundPeers(fundId);

  if (fundLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <LoaderIcon className="h-8 w-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Loading fund details...</p>
        </div>
      </div>
    );
  }

  if (fundError || !fund) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">
            Fund not found or error loading data
          </p>
          <Link href="/">
            <Button>Back to Dashboard</Button>
          </Link>
        </div>
      </div>
    );
  }

  const currentValue = fund.current_value
    ? parseFloat(fund.current_value)
    : parseFloat(fund.total_aum);
  const unrealizedGainLoss = parseFloat(fund.unrealized_gain_loss);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white shadow-lg border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <Link href="/">
                <Button variant="ghost" size="sm">
                  <ArrowLeftIcon className="h-4 w-4 mr-2" />
                  Back
                </Button>
              </Link>
              <div>
                <h1 className="text-xl font-bold text-gray-900">{fund.name}</h1>
                <p className="text-sm text-gray-500">
                  {fund.manager_name} • Inception:{" "}
                  {formatDate(fund.inception_date)}
                </p>
              </div>
            </div>
            <Badge variant="outline" className="text-sm bg-blue-500/20">
              {fund.strategy.charAt(0).toUpperCase() +
                fund.strategy.slice(1).replace("_", " ")}
            </Badge>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Fund Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/20 hover:scale-[1.02]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total AUM</CardTitle>
              <DollarSignIcon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(parseFloat(fund.total_aum))}
              </div>
              <p className="text-xs text-muted-foreground">
                Assets Under Management
              </p>
            </CardContent>
          </Card>

          <Card className="transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/20 hover:scale-[1.02]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Current Value
              </CardTitle>
              <TrendingUpIcon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(currentValue)}
              </div>
              <p className="text-xs text-muted-foreground">
                Market value today
              </p>
            </CardContent>
          </Card>

          <Card className="transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/20 hover:scale-[1.02]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Unrealized P&L
              </CardTitle>
              <BarChart3Icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div
                className={`text-2xl font-bold ${unrealizedGainLoss >= 0 ? "text-green-600" : "text-red-600"}`}
              >
                {formatCurrency(unrealizedGainLoss)}
              </div>
              <p className="text-xs text-muted-foreground">
                {formatPercent(fund.unrealized_gain_loss_percent)}
              </p>
            </CardContent>
          </Card>

          <Card className="transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/20 hover:scale-[1.02]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Holdings</CardTitle>
              <FolderIcon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{fund.holdings_count}</div>
              <p className="text-xs text-muted-foreground">
                Individual positions
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Holdings Table */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Holdings</CardTitle>
            <CardDescription>
              Individual stock positions within this fund
            </CardDescription>
          </CardHeader>
          <CardContent>
            {holdingsLoading ? (
              <div className="text-center py-8">
                <LoaderIcon className="h-6 w-6 animate-spin mx-auto mb-2 text-blue-600" />
                <p className="text-gray-600">Loading holdings...</p>
              </div>
            ) : holdings.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-600">No holdings data available</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left py-3 px-2 font-medium">
                        Ticker
                      </th>
                      <th className="text-left py-3 px-2 font-medium">
                        Company
                      </th>
                      <th className="text-right py-3 px-2 font-medium">
                        Shares
                      </th>
                      <th className="text-right py-3 px-2 font-medium">
                        Purchase Price
                      </th>
                      <th className="text-right py-3 px-2 font-medium">
                        Cost Basis
                      </th>
                      <th className="text-right py-3 px-2 font-medium">
                        Current Value
                      </th>
                      <th className="text-left py-3 px-2 font-medium">
                        Sector
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {holdings.map((holding) => {
                      const costBasis = parseFloat(holding.cost_basis);
                      const currentValue = holding.current_value
                        ? parseFloat(holding.current_value)
                        : costBasis;

                      return (
                        <tr
                          key={holding.id}
                          className="border-b hover:bg-gray-50 dark:hover:bg-gray-800"
                        >
                          <td className="py-3 px-2 font-medium text-blue-600">
                            {holding.ticker}
                          </td>
                          <td className="py-3 px-2">
                            {holding.company_name || "N/A"}
                          </td>
                          <td className="py-3 px-2 text-right">
                            {parseFloat(holding.shares).toLocaleString()}
                          </td>
                          <td className="py-3 px-2 text-right">
                            ${parseFloat(holding.purchase_price).toFixed(2)}
                          </td>
                          <td className="py-3 px-2 text-right">
                            {formatCurrency(costBasis)}
                          </td>
                          <td className="py-3 px-2 text-right font-medium">
                            {formatCurrency(currentValue)}
                          </td>
                          <td className="py-3 px-2">
                            {holding.sector ? (
                              <Badge variant="outline" className="text-xs">
                                {holding.sector}
                              </Badge>
                            ) : (
                              "N/A"
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Performance and Peers Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Performance Chart Placeholder */}
          <Card>
            <CardHeader>
              <CardTitle>Performance</CardTitle>
              <CardDescription>
                Fund performance over the last 90 days
              </CardDescription>
            </CardHeader>
            <CardContent>
              {performanceLoading ? (
                <div className="text-center py-8">
                  <LoaderIcon className="h-6 w-6 animate-spin mx-auto mb-2 text-blue-600" />
                  <p className="text-gray-600">Loading performance data...</p>
                </div>
              ) : !performance || performance.performance_data.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-gray-600">No performance data available</p>
                </div>
              ) : (
                <PerformanceChart
                  data={performance.performance_data}
                  fundName={fund.name}
                />
              )}
            </CardContent>
          </Card>

          {/* Peer Comparison */}
          <Card>
            <CardHeader>
              <CardTitle>Peer Comparison</CardTitle>
              <CardDescription>
                How this fund compares to similar funds
              </CardDescription>
            </CardHeader>
            <CardContent>
              {peersLoading ? (
                <div className="text-center py-8">
                  <LoaderIcon className="h-6 w-6 animate-spin mx-auto mb-2 text-blue-600" />
                  <p className="text-gray-600">Loading peer data...</p>
                </div>
              ) : !peers || peers.peers.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-gray-600">
                    No peer comparison data available
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  <PeerComparisonChart
                    peers={peers.peers}
                    currentFund={{
                      name: fund.name,
                      performance: fund.total_return_percent,
                    }}
                  />
                  <div className="mt-4 space-y-2">
                    {peers.peers.slice(0, 3).map((peer) => (
                      <div
                        key={peer.fund_id}
                        className="flex justify-between items-center py-2 border-b border-gray-100"
                      >
                        <div>
                          <p className="font-medium text-sm">
                            {peer.fund_name}
                          </p>
                          <p className="text-xs text-gray-500">
                            {peer.benchmark_category
                              .replace(/_/g, " ")
                              .replace(/\b\w/g, (l) => l.toUpperCase())}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-medium">
                            {peer.total_aum
                              ? formatCurrency(parseFloat(peer.total_aum))
                              : "N/A"}
                          </p>
                          <p
                            className={`text-xs font-medium ${(peer.total_return || 0) >= 0 ? "text-green-600" : "text-red-600"}`}
                          >
                            {peer.total_return != null
                              ? `${peer.total_return >= 0 ? "+" : ""}${Number(peer.total_return).toFixed(2)}%`
                              : "N/A"}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
