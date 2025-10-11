"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Package } from "lucide-react";
import Link from "next/link";
import { createClient } from "@/lib/supabase/client";

type HelloResponse = {
  message: string;
};

export default function HomePage() {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [djangoMessage, setDjangoMessage] = useState<string>(""); // new state

  useEffect(() => {
    const checkAuth = async () => {
      const supabase = createClient();
      const {
        data: { user },
      } = await supabase.auth.getUser();

      if (user) {
        router.push("/inventory");
        return;
      }

      setIsLoggedIn(false);
      setIsLoading(false);
    };

    const fetchDjango = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/hello/");
        const data: HelloResponse = await res.json();
        setDjangoMessage(data.message);
      } catch (error) {
        console.error("Error fetching from Django:", error);
      }
    };

    checkAuth();
    fetchDjango(); //fetch from Django
  }, [router]);

  if (isLoading) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Package className="h-6 w-6 text-blue-600" />
            <span className="font-bold text-xl">InvoiceBI</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/auth/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/auth/signup">
              <Button>Sign Up</Button>
            </Link>
          </div>
        </div>
      </header>

      <div className="container mx-auto py-16 px-4">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-foreground mb-4">
            Inventory & Invoice Management
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Complete business solution for inventory tracking, invoice
            generation, and intelligent analytics
          </p>
          {/* Example: showing Django API data */}
          {djangoMessage && (
            <p className="mt-4 text-blue-600 font-semibold">{djangoMessage}</p>
          )}
        </div>

        <div className="bg-blue-600 text-white rounded-2xl p-8 text-center">
          <h2 className="text-3xl font-bold mb-4">
            Ready to streamline your business?
          </h2>
          <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
            Start managing your inventory, creating invoices, and analyzing your
            business performance all in one place.
          </p>
          <Link href="/auth/login">
            <Button
              size="lg"
              variant="secondary"
              className="bg-white text-blue-600 hover:bg-blue-50">
              Get Started
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
