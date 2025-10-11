"use client"

import { useState, useEffect } from "react"
import { calculateSalesData, getLowStockItems, calculateRevenueByDate, calculateTotalStats } from "@/lib/analytics"
import { StatsCards } from "@/components/dashboard/stats-cards"
import { TopProducts } from "@/components/dashboard/top-products"
import { RevenueChart } from "@/components/dashboard/revenue-chart"
import { LowStockAlert } from "@/components/dashboard/low-stock-alert"
import { BarChart3, Menu } from "lucide-react"
import { Sidebar } from "@/components/navigation/sidebar"
import { Button } from "@/components/ui/button"

export default function DashboardPage() {
  const [mounted, setMounted] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    totalRevenue: 0,
    totalInvoices: 0,
    totalProducts: 0,
    lowStockCount: 0,
  })
  const [salesData, setSalesData] = useState<ReturnType<typeof calculateSalesData>>([])
  const [lowStockItems, setLowStockItems] = useState<ReturnType<typeof getLowStockItems>>([])
  const [revenueData, setRevenueData] = useState<ReturnType<typeof calculateRevenueByDate>>([])

  useEffect(() => {
    setMounted(true)
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    setLoading(true)
    try {
      const [statsData, sales, lowStock, revenue] = await Promise.all([
        calculateTotalStats(),
        calculateSalesData(),
        getLowStockItems(),
        calculateRevenueByDate(),
      ])
      setStats(statsData)
      setSalesData(sales)
      setLowStockItems(lowStock)
      setRevenueData(revenue)
    } catch (error) {
      console.error("Error loading dashboard data:", error)
    } finally {
      setLoading(false)
    }
  }

  if (!mounted) {
    return null
  }

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen} />

      <main className="flex-1 p-8">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Button
              variant="outline"
              size="icon"
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="bg-white hover:bg-gray-50 text-gray-700 shadow-sm border"
            >
              <Menu className="h-5 w-5" />
            </Button>
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-600 text-white">
              <BarChart3 className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-foreground">Business Intelligence</h1>
              <p className="text-muted-foreground">Analytics and insights for your business</p>
            </div>
          </div>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <p className="text-muted-foreground">Loading dashboard data...</p>
          </div>
        ) : (
          <div className="space-y-6">
            <StatsCards stats={stats} />

            <div className="grid gap-6 lg:grid-cols-2">
              <RevenueChart data={revenueData} />
              <TopProducts salesData={salesData} />
            </div>

            <LowStockAlert items={lowStockItems} />
          </div>
        )}
      </main>
    </div>
  )
}
