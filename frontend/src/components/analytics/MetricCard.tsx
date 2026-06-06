"use client"

import React from "react"

interface MetricCardProps {
  title: string
  value: string | number
  description?: string
  trend?: string
}

export default function MetricCard({
  title,
  value,
  description,
  trend
}: MetricCardProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6 shadow-xl transition-all duration-200 hover:border-zinc-700/60 selection:bg-indigo-600">
      <div className="flex flex-col space-y-2">
        {/* Card Header Title Label */}
        <p className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">
          {title}
        </p>
        
        {/* Core Value Metric Unit */}
        <div className="flex items-baseline justify-between">
          <h2 className="text-3xl font-bold tracking-tight text-zinc-100">
            {value}
          </h2>
          {trend && (
            <span className="text-xs font-medium text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-md">
              {trend}
            </span>
          )}
        </div>

        {/* Optional Secondary Context Note */}
        {description && (
          <p className="text-xs text-zinc-500 font-light pt-1 leading-relaxed">
            {description}
          </p>
        )}
      </div>
    </div>
  )
}
