export interface InventoryItem {
  id: string
  name: string
  description: string
  sku: string
  category: string
  price: number
  discount: number // percentage
  stock: number
  minStock: number // for low stock alerts
  imageUrl?: string // renamed from image to imageUrl for clarity
  userId?: string // added userId for RLS
  createdAt: string
  updatedAt: string
}

export interface InvoiceItem {
  id: string
  inventoryItemId: string
  name: string
  sku: string
  quantity: number
  price: number
  discount: number
  total: number
}

export interface Invoice {
  id: string
  invoiceNumber: string
  customerName: string
  customerEmail: string
  customerPhone: string
  items: InvoiceItem[]
  subtotal: number
  tax: number
  discount: number
  total: number
  status: "draft" | "paid" | "cancelled"
  createdAt: string
  updatedAt: string
}

export interface SalesData {
  itemId: string
  itemName: string
  totalQuantity: number
  totalRevenue: number
  invoiceCount: number
}
