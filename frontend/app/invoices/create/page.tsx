"use client"

import { useRouter } from "next/navigation"
import { CreateInvoiceForm } from "@/components/invoice/create-invoice-form"
import { addInvoice } from "@/lib/supabase-storage"
import { Button } from "@/components/ui/button"
import { ArrowLeft } from "lucide-react"
import Link from "next/link"
import { useState } from "react"

export default function CreateInvoicePage() {
  const router = useRouter()
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (data: Parameters<typeof addInvoice>[0]) => {
    try {
      setIsSubmitting(true)
      const result = await addInvoice(data)
      if (result) {
        alert("Invoice created successfully!")
        router.push("/invoices")
      } else {
        alert("Failed to create invoice. Please check stock availability.")
      }
    } catch (error) {
      console.error("Error creating invoice:", error)
      alert("Failed to create invoice. Please try again.")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto py-8 px-4">
        <div className="mb-8">
          <Link href="/invoices">
            <Button variant="ghost" size="sm" className="mb-4">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Invoices
            </Button>
          </Link>
          <h1 className="text-3xl font-bold text-foreground">Create New Invoice</h1>
          <p className="text-muted-foreground">Fill in the details to generate a new invoice</p>
        </div>

        {isSubmitting && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-background p-6 rounded-lg shadow-lg text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-foreground">Creating invoice...</p>
            </div>
          </div>
        )}

        <CreateInvoiceForm onSubmit={handleSubmit} />
      </div>
    </div>
  )
}
