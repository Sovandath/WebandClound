"use client"

import { useState, useEffect } from "react"
import type { Invoice } from "@/types"
import { getInvoices } from "@/lib/supabase-storage"
import { InvoiceList } from "@/components/invoice/invoice-list"
import { Button } from "@/components/ui/button"
import { FileText, Plus, Menu } from "lucide-react"
import Link from "next/link"
import { Sidebar } from "@/components/navigation/sidebar"

export default function InvoicesPage() {
  const [invoices, setInvoices] = useState<Invoice[]>([])
  const [mounted, setMounted] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setMounted(true)
    loadInvoices()
  }, [])

  const loadInvoices = async () => {
    setLoading(true)
    try {
      const loadedInvoices = await getInvoices()
      setInvoices(loadedInvoices)
    } catch (error) {
      console.error("Error loading invoices:", error)
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
        <div className="mb-8 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="icon"
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="bg-white hover:bg-gray-50 text-gray-700 shadow-sm border"
            >
              <Menu className="h-5 w-5" />
            </Button>
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-600 text-white">
              <FileText className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-foreground">Invoices</h1>
              <p className="text-muted-foreground">Manage and export your invoices</p>
            </div>
          </div>
          <Link href="/invoices/create">
            <Button className="bg-blue-600 hover:bg-blue-700">
              <Plus className="mr-2 h-4 w-4" />
              Create Invoice
            </Button>
          </Link>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <p className="text-muted-foreground">Loading invoices...</p>
          </div>
        ) : (
          <InvoiceList invoices={invoices} onUpdate={loadInvoices} />
        )}
      </main>
    </div>
  )
}
