"use client"

import React, { useMemo } from "react"
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts"

interface RetrievalCardProps {
  evaluations: any[]
}

export default function RetrievalCard({ evaluations }: RetrievalCardProps) {
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
        score: e.avg_rerank_score || 0
      }))
  }, [evaluations])

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 shadow-xl transition-all duration-200 hover:border-zinc-800/80 h-[400px] flex flex-col justify-between selection:bg-indigo-600 select-none">
      {/* Chart Title Meta Section */}
      <div className="mb-4">
        <h3 className="text-sm font-semibold text-zinc-200 uppercase tracking-wider">
          Retrieval Context Relevance Quality
        </h3>
        <p className="text-xs text-zinc-500 font-light mt-0.5 leading-relaxed">
          Cross-Encoder evaluation analytics scores tracking semantic grounding confidence
        </p>
      </div>

      {/* Recharts Canvas Section */}
      <div className="flex-1 w-full text-[10px] font-medium font-mono text-zinc-500 relative pr-4">
        {data.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 10, right: 5, left: -25, bottom: 5 }}>
              <defs>
                <linearGradient id="scoreGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0.1}/>
                </linearGradient>
              </defs>
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
                domain={[0, 1]}
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
                itemStyle={{ color: "#34d399" }}
                labelStyle={{ color: "#71717a", fontWeight: "bold", marginBottom: "4px" }}
                cursor={{ fill: "#18181b", opacity: 0.4 }}
              />
              <Bar 
                dataKey="score" 
                fill="url(#scoreGradient)" 
                stroke="#10b981"
                strokeWidth={1}
                radius={[4, 4, 0, 0]}
                name="Rerank Confidence Score"
              />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="absolute inset-0 flex items-center justify-center text-center opacity-40">
            <p className="text-xs text-zinc-400 font-light tracking-wide">
              Awaiting inbound context retrieval logs to calculate relevance maps...
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
