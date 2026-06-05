import React from "react"
import "../globals.css"  // 👈 Added an extra dot to step up into the parent src/ folder

export const metadata = {
  title: "AI Research Assistant",
  description: "Enterprise multi-document workspace AI assistant platform",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-zinc-950 text-zinc-100 antialiased min-h-screen">
        {children}
      </body>
    </html>
  )
}
