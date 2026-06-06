"use client"

import React, { useMemo } from "react"
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts"

interface LatencyCardProps {
  evaluations: any[]
}

export default function LatencyCard({ evaluations }: LatencyCardProps) {
  // Chronologically sort data records to render line vectors smoothly from past to present
  const data = useMemo(() => {
    if (!evaluations || evaluations.length === 0) return []
    
    return [...evaluations]
      .reverse() // Flip chronological order array layout cleanly
      .map((e: any) => ({
        time: new Date(e.created_at).toLocaleDateString(undefined, {
          month: "short",
          day: "numeric"
        }),
        latency: e.total_latency_ms || 0,
        retrieval: e.retrieval_latency_ms || 0,
        llm: e.llm_latency_ms || 0
      }))
  }, [evaluations])

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 shadow-xl transition-all duration-200 hover:border-zinc-800/80 h-[400px] flex flex-col justify-between selection:bg-indigo-600 select-none">
      {/* Chart Title Meta Section */}
      <div className="mb-4">
        <h3 className="text-sm font-semibold text-zinc-200 uppercase tracking-wider">
          Request Latency Tracing
        </h3>
        <p className="text-xs text-zinc-500 font-light mt-0.5 leading-relaxed">
          End-to-end turnaround execution duration distributed in milliseconds
        </p>
      </div>

      {/* Recharts Canvas Section */}
      <div className="flex-1 w-full text-[10px] font-medium font-mono text-zinc-500 relative pr-4">
        {data.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 10, right: 5, left: -20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
              <XAxis 
                dataKey="time" 
                stroke="#52525b" 
                tickLine={false} 
                dy={10} 
              />
              <YAxis 
                stroke="#52525b" 
                tickLine={false} 
                dx={-5}
                unit="ms"
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: "#09090b", 
                  borderColor: "#27272a", 
                  borderRadius: "8px",
                  color: "#f4f4f5",
                  fontSize: "12px",
                  fontFamily: "monospace"
                }}
                itemStyle={{ color: "#a5b4fc" }}
                labelStyle={{ color: "#71717a", fontWeight: "bold", marginBottom: "4px" }}
                cursor={{ stroke: "#3f3f46", strokeWidth: 1 }}
              />
              <Line 
                type="monotone" 
                dataKey="latency" 
                stroke="#6366f1" 
                strokeWidth={2.5}
                dot={{ fill: "#6366f1", stroke: "#09090b", strokeWidth: 2, r: 4 }}
                activeDot={{ fill: "#fff", stroke: "#6366f1", strokeWidth: 2, r: 6 }}
                name="Total Response Time"
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="absolute inset-0 flex items-center justify-center text-center opacity-40">
            <p className="text-xs text-zinc-400 font-light tracking-wide">
              Awaiting inbound log traces to compute latency curves...
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
