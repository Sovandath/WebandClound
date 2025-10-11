import type { InventoryItem, SalesData } from "@/types"
import { getInvoices, getInventoryItems } from "./supabase-storage"

export const calculateSalesData = async (): Promise<SalesData[]> => {
  const invoices = await getInvoices()
  const salesMap = new Map<string, SalesData>()

  invoices.forEach((invoice) => {
    if (invoice.status === "paid") {
      invoice.items.forEach((item: any) => {
        const existing = salesMap.get(item.inventoryItemId)
        if (existing) {
          existing.totalQuantity += item.quantity
          existing.totalRevenue += item.total
          existing.invoiceCount += 1
        } else {
          salesMap.set(item.inventoryItemId, {
            itemId: item.inventoryItemId,
            itemName: item.name,
            totalQuantity: item.quantity,
            totalRevenue: item.total,
            invoiceCount: 1,
          })
        }
      })
    }
  })

  return Array.from(salesMap.values()).sort((a, b) => b.totalRevenue - a.totalRevenue)
}

export const getLowStockItems = async (): Promise<InventoryItem[]> => {
  const items = await getInventoryItems()
  return items.filter((item) => item.stock <= item.minStock).sort((a, b) => a.stock - b.stock)
}

export const calculateRevenueByDate = async (): Promise<{ date: string; revenue: number; invoices: number }[]> => {
  const invoices = await getInvoices()
  const paidInvoices = invoices.filter((inv) => inv.status === "paid")
  const revenueMap = new Map<string, { revenue: number; invoices: number }>()

  paidInvoices.forEach((invoice) => {
    const date = new Date(invoice.createdAt).toLocaleDateString()
    const existing = revenueMap.get(date)
    if (existing) {
      existing.revenue += invoice.total
      existing.invoices += 1
    } else {
      revenueMap.set(date, { revenue: invoice.total, invoices: 1 })
    }
  })

  return Array.from(revenueMap.entries())
    .map(([date, data]) => ({ date, ...data }))
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
}

export const calculateTotalStats = async () => {
  const invoices = await getInvoices()
  const items = await getInventoryItems()

  const totalRevenue = invoices.filter((inv) => inv.status === "paid").reduce((sum, inv) => sum + inv.total, 0)

  const totalInvoices = invoices.filter((inv) => inv.status === "paid").length
  const totalProducts = items.length
  const lowStockCount = items.filter((item) => item.stock <= item.minStock).length

  return {
    totalRevenue,
    totalInvoices,
    totalProducts,
    lowStockCount,
  }
}
