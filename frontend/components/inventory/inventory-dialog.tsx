"use client"

import type { InventoryItem } from "@/types"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"
import { InventoryForm } from "./inventory-form"
import { addInventoryItem, updateInventoryItem } from "@/lib/supabase-storage"

interface InventoryDialogProps {
  item?: InventoryItem | null
  open?: boolean
  onOpenChange?: (open: boolean) => void
  onSuccess: () => void
}

export function InventoryDialog({ item, open, onOpenChange, onSuccess }: InventoryDialogProps) {
  const handleSubmit = async (data: Omit<InventoryItem, "id" | "createdAt" | "updatedAt" | "userId">) => {
    if (item) {
      await updateInventoryItem(item.id, data)
    } else {
      await addInventoryItem(data)
    }
    onSuccess()
  }

  const handleCancel = () => {
    if (onOpenChange) {
      onOpenChange(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      {!item && (
        <DialogTrigger asChild>
          <Button className="bg-blue-600 hover:bg-blue-700">
            <Plus className="mr-2 h-4 w-4" />
            Add Item
          </Button>
        </DialogTrigger>
      )}
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{item ? "Edit Item" : "Add New Item"}</DialogTitle>
          <DialogDescription>
            {item ? "Update the inventory item details below." : "Fill in the details to add a new item to inventory."}
          </DialogDescription>
        </DialogHeader>
        <InventoryForm item={item} onSubmit={handleSubmit} onCancel={handleCancel} />
      </DialogContent>
    </Dialog>
  )
}
