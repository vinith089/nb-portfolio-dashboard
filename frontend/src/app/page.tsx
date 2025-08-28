"use client";
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
  ArrowUpIcon,
  ArrowDownIcon,
  TrendingUpIcon,
  FolderIcon,
  DollarSignIcon,
  LoaderIcon,
  ArrowRightIcon,
} from "lucide-react";
import { useFunds } from "@/hooks/useFunds";
import { formatCurrency, formatPercent } from "@/lib/api";
import { FundPreviewModal } from "@/components/FundPreviewModal";
import { FraudAlertBanner } from "@/components/FraudAlertBanner";

export default function DashboardPage() {
  const { funds, loading, error } = useFunds();

  // Show loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <LoaderIcon className="h-8 w-8 animate-spin mx-auto mb-4 text-blue-800" />
          <p className="text-gray-600 ">Loading portfolio data...</p>
        </div>
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">Error loading data: {error}</p>
          <Button onClick={() => window.location.reload()}>Retry</Button>
        </div>
      </div>
    );
  }

  // Calculate portfolio totals from API data
  const portfolioTotals = funds.reduce(
    (acc, fund) => {
      const totalAUM = parseFloat(fund.total_aum);
      const currentValue = fund.current_value
        ? parseFloat(fund.current_value)
        : totalAUM;

      return {
        totalAUM: acc.totalAUM + totalAUM,
        currentValue: acc.currentValue + currentValue,
        totalFunds: acc.totalFunds + 1,
        totalHoldings: acc.totalHoldings + fund.holdings_count,
      };
    },
    { totalAUM: 0, currentValue: 0, totalFunds: 0, totalHoldings: 0 }
  );

  const portfolioReturn =
    portfolioTotals.totalAUM > 0
      ? ((portfolioTotals.currentValue - portfolioTotals.totalAUM) /
          portfolioTotals.totalAUM) *
        100
      : 0;

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white shadow-lg border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <TrendingUpIcon className="h-6 w-6 md:h-8 md:w-8 text-slate-600" />
              <h1 className="text-lg md:text-2xl font-semibold md:font-bold text-gray-900">
                Portfolio Dashboard
              </h1>
            </div>
            <img
              src="/images/nb_standard_logo_black.svg"
              alt="Neuberger Berman"
              className="h-8 md:h-10 w-auto"
            />
          </div>
        </div>
      </header>

      {/* Fraud Alert Banner */}
      <FraudAlertBanner />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Portfolio Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/20 hover:scale-[1.02]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total AUM</CardTitle>
              <DollarSignIcon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(portfolioTotals.totalAUM)}
              </div>
              <p className="text-xs text-muted-foreground">
                Across {portfolioTotals.totalFunds} funds
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
                {formatCurrency(portfolioTotals.currentValue)}
              </div>
              <p className="text-xs text-muted-foreground">
                Market value today
              </p>
            </CardContent>
          </Card>

          <Card className="transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/20 hover:scale-[1.02]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Portfolio Return
              </CardTitle>
              {portfolioReturn >= 0 ? (
                <ArrowUpIcon className="h-4 w-4 text-green-600" />
              ) : (
                <ArrowDownIcon className="h-4 w-4 text-red-600" />
              )}
            </CardHeader>
            <CardContent>
              <div
                className={`text-2xl font-bold ${portfolioReturn >= 0 ? "text-green-600" : "text-red-600"}`}
              >
                {formatPercent(portfolioReturn)}
              </div>
              <p className="text-xs text-muted-foreground">
                Total unrealized gain
              </p>
            </CardContent>
          </Card>

          <Card className="transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/20 hover:scale-[1.02]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Holdings
              </CardTitle>
              <FolderIcon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {portfolioTotals.totalHoldings}
              </div>
              <p className="text-xs text-muted-foreground">
                Individual positions
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Funds List */}
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold">Fund Performance</h2>
          </div>

          <div className="grid gap-4">
            {funds.map((fund) => {
              const currentValue = fund.current_value
                ? parseFloat(fund.current_value)
                : parseFloat(fund.total_aum);
              const totalReturn = fund.total_return_percent || 0;
              const dailyReturn = fund.daily_return_percent || 0;

              return (
                <Card
                  key={fund.id}
                  className="hover:shadow-md transition-shadow"
                >
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-lg">{fund.name}</CardTitle>
                        <CardDescription className="flex items-center space-x-2 mt-1">
                          <Badge variant="secondary" className="text-xs">
                            {fund.strategy.charAt(0).toUpperCase() +
                              fund.strategy.slice(1).replace("_", " ")}
                          </Badge>
                          <span className="text-sm text-muted-foreground">
                            {fund.holdings_count} holdings
                          </span>
                        </CardDescription>
                      </div>
                      <div className="text-right">
                        <div className="text-lg font-semibold">
                          {formatCurrency(currentValue)}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          AUM: {formatCurrency(parseFloat(fund.total_aum))}
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="flex justify-between items-center">
                      <div className="flex space-x-4">
                        <div>
                          <div className="text-sm text-muted-foreground">
                            Total Return
                          </div>
                          <div
                            className={`font-medium ${totalReturn >= 0 ? "text-green-600" : "text-red-600"}`}
                          >
                            {formatPercent(totalReturn)}
                          </div>
                        </div>
                        <div>
                          <div className="text-sm text-muted-foreground">
                            Daily Return
                          </div>
                          <div
                            className={`font-medium flex items-center ${dailyReturn >= 0 ? "text-green-600" : "text-red-600"}`}
                          >
                            {dailyReturn >= 0 ? (
                              <ArrowUpIcon className="h-3 w-3 mr-1" />
                            ) : (
                              <ArrowDownIcon className="h-3 w-3 mr-1" />
                            )}
                            {formatPercent(dailyReturn)}
                          </div>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <FundPreviewModal fund={fund}>
                          <Button variant="outline" size="sm">
                            Preview
                          </Button>
                        </FundPreviewModal>
                        <Link href={`/funds/${fund.id}`}>
                          <Button
                            size="sm"
                            className="bg-slate-800 hover:bg-slate-600"
                          >
                            View Full Details{" "}
                            <ArrowRightIcon className="ml-2 h-4 w-4" />
                          </Button>
                        </Link>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </main>
    </div>
  );
}
