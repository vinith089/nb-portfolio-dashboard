"use client";

import { useState, useEffect } from "react";
import { AlertTriangleIcon, XIcon } from "lucide-react";
import { Button } from "@/components/ui/button";

export function FraudAlertBanner() {
  const [isVisible, setIsVisible] = useState(false);
  const [shouldRender, setShouldRender] = useState(false);

  useEffect(() => {
    // Check if user has previously dismissed the banner
    const dismissed = localStorage.getItem("fraud-alert-dismissed");
    if (dismissed) {
      return;
    }

    // Start rendering the banner (but hidden)
    setShouldRender(true);

    // Show banner after 2 seconds
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  const handleDismiss = () => {
    setIsVisible(false);
    // Remember dismissal in localStorage
    localStorage.setItem("fraud-alert-dismissed", "true");
    // Remove from DOM after animation completes
    setTimeout(() => setShouldRender(false), 500);
  };

  if (!shouldRender) {
    return null;
  }

  return (
    <div
      className={`relative z-40 bg-slate-900 border-b border-slate-700 transition-all duration-500 ease-out ${
        isVisible
          ? "transform translate-y-0 opacity-100"
          : "transform -translate-y-full opacity-0"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between py-3">
          <div className="flex items-center space-x-3">
            <AlertTriangleIcon className="h-8 w-8 text-orange-400 flex-shrink-0" />
            <div className="text-sm text-white">
              <span className="font-semibold text-orange-400">
                IMPORTANT NOTICE - FRAUD ALERT:
              </span>
              <div className="">
                NB does not solicit/conduct business via third party messaging
                apps such as WhatsApp, Line, Facebook etc.
              </div>
            </div>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleDismiss}
            className="text-white hover:text-gray-300 hover:bg-slate-700 p-1"
          >
            <XIcon className="h-4 w-4" />
            <span className="sr-only">Dismiss alert</span>
          </Button>
        </div>
      </div>
    </div>
  );
}
