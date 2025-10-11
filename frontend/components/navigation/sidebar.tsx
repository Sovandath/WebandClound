"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { X, Package, FileText, BarChart3, Home } from "lucide-react"
import { Button } from "@/components/ui/button"
import { UserMenu } from "@/components/auth/user-menu"
import { cn } from "@/lib/utils"

const navItems = [
  {
    title: "Inventory Management",
    href: "/inventory",
    icon: Package,
  },
  {
    title: "Invoice Generation",
    href: "/invoices",
    icon: FileText,
  },
  {
    title: "Business Intelligence",
    href: "/dashboard",
    icon: BarChart3,
  },
]

interface SidebarProps {
  isOpen: boolean
  setIsOpen: (open: boolean) => void
}

export function Sidebar({ isOpen, setIsOpen }: SidebarProps) {
  const pathname = usePathname()

  return (
    <>
      {isOpen && <div className="fixed inset-0 bg-black/50 z-40" onClick={() => setIsOpen(false)} />}

      <aside
        className={cn(
          "fixed top-0 left-0 z-40 h-screen w-64 bg-background border-r transition-transform duration-300 ease-in-out",
          isOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="flex flex-col h-full">
          <div className="p-6 border-b flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2 text-xl font-bold text-blue-600">
              <Home className="h-6 w-6" />
              <span>Inventory BI</span>
            </Link>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsOpen(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>

          <nav className="flex-1 p-4 space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = pathname === item.href || (item.href !== "/" && pathname?.startsWith(item.href + "/"))

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className={cn(
                    "flex items-center gap-3 px-4 py-3 rounded-lg transition-colors",
                    isActive
                      ? "bg-blue-600 text-white"
                      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
                  )}
                >
                  <Icon className="h-5 w-5" />
                  <span className="font-medium">{item.title}</span>
                </Link>
              )
            })}
          </nav>

          <div className="p-4 border-t">
            <UserMenu />
          </div>
        </div>
      </aside>
    </>
  )
}
