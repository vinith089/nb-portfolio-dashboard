"use client";

import Link from "next/link";
import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  TrendingUpIcon,
  DollarSignIcon,
  FolderIcon,
  ExternalLinkIcon,
} from "lucide-react";
import { useFundHoldings } from "@/hooks/useFunds";
import { formatCurrency, formatPercent, Fund } from "@/lib/api";

interface FundPreviewModalProps {
  fund: Fund;
  children: React.ReactNode;
}

export function FundPreviewModal({ fund, children }: FundPreviewModalProps) {
  const [open, setOpen] = useState(false);
  const { holdings, loading: holdingsLoading } = useFundHoldings(fund.id);

  const currentValue = parseFloat(fund.current_value || fund.total_aum);
  const totalReturn = fund.total_return_percent ?? 0;
  const dailyReturn = fund.daily_return_percent ?? 0;

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center justify-between mt-4">
            <span>{fund.name}</span>
            <Badge variant="outline" className="ml-2 bg-blue-500/20">
              {fund.strategy.charAt(0).toUpperCase() +
                fund.strategy.slice(1).replace("_", " ")}
            </Badge>
          </DialogTitle>
        </DialogHeader>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          {/* Key Metrics */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Current Value
              </CardTitle>
              <DollarSignIcon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(currentValue)}
              </div>
              <p className="text-xs text-muted-foreground">
                AUM: {formatCurrency(parseFloat(fund.total_aum))}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Return
              </CardTitle>
              <TrendingUpIcon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div
                className={`text-2xl font-bold ${
                  totalReturn >= 0 ? "text-green-600" : "text-red-600"
                }`}
              >
                {formatPercent(totalReturn)}
              </div>
              <p
                className={`text-xs font-medium ${
                  dailyReturn >= 0 ? "text-green-600" : "text-red-600"
                }`}
              >
                Daily: {formatPercent(dailyReturn)}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Holdings</CardTitle>
              <FolderIcon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{fund.holdings_count}</div>
              <p className="text-xs text-muted-foreground">
                Expense Ratio:{" "}
                {parseFloat(fund.expense_ratio || "0").toFixed(2)}%
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Top Holdings Preview */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Top Holdings</CardTitle>
          </CardHeader>
          <CardContent>
            {holdingsLoading ? (
              <div className="text-center py-4">
                <p className="text-gray-600">Loading holdings...</p>
              </div>
            ) : !holdings || holdings.length === 0 ? (
              <div className="text-center py-4">
                <p className="text-gray-600">No holdings data available</p>
              </div>
            ) : (
              <div className="space-y-3">
                {holdings.slice(0, 6).map((holding) => {
                  const costBasis = parseFloat(holding.cost_basis);
                  const currentValue = holding.current_value
                    ? parseFloat(holding.current_value)
                    : costBasis;

                  return (
                    <div
                      key={holding.id}
                      className="flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0"
                    >
                      <div>
                        <p className="font-medium text-blue-600">
                          {holding.ticker}
                        </p>
                        <p className="text-sm text-gray-600">
                          {holding.company_name || "N/A"}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-medium">
                          {formatCurrency(currentValue)}
                        </p>
                        <p className="text-sm text-gray-500">
                          {parseFloat(holding.shares).toLocaleString()} shares
                        </p>
                      </div>
                    </div>
                  );
                })}
                {holdings.length > 6 && (
                  <p className="text-sm text-gray-500 text-center pt-2">
                    + {holdings.length - 6} more holdings
                  </p>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Footer Actions */}
        <div className="flex justify-between items-center pt-4 border-t">
          <div className="text-sm text-gray-600">
            <p>Manager: {fund.manager_name || "N/A"}</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={() => setOpen(false)}>
              Close
            </Button>
            <Link href={`/funds/${fund.id}`}>
              <Button className="flex items-center gap-2 bg-slate-800 hover:bg-slate-600">
                View Full Details
                <ExternalLinkIcon className="h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
