import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"  // 👈 Swapped next/request for next/server

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // 1. Unpack the session authentication state out of the browser's secure cookies panel
  const authToken = request.cookies.get("auth_token")?.value

  // Define route classifications
  const isAuthPage = pathname.startsWith("/login") || pathname.startsWith("/register")
  const isProtectedPage = pathname === "/" || pathname.startsWith("/dashboard") || pathname.startsWith("/workspaces") || pathname.startsWith("/chat")

  // 🛡️ Security Check A: If an anonymous user tries to sneak into app workspace views, kick them to login
  if (!authToken && isProtectedPage) {
    const loginUrl = new URL("/login", request.url)
    return NextResponse.redirect(loginUrl)
  }

  // 🛡️ Security Check B: If an already authenticated user visits /login or /register, redirect them straight to the main app dashboard
  if (authToken && isAuthPage) {
    const dashboardUrl = new URL("/", request.url) // Pointing to your main home dashboard layout screen space
    return NextResponse.redirect(dashboardUrl)
  }

  // Let the client move to their desired destination page route uninterrupted
  return NextResponse.next()
}

// 🎯 Strict Optimization Matcher List Filter Config:
// Directs Next.js to skip assets, image logs, and internal API files to maintain speed
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
}
