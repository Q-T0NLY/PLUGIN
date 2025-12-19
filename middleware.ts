import { createMiddlewareClient } from "@/lib/supabase/middleware"
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export async function middleware(request: NextRequest) {
  const { response, supabase } = await createMiddlewareClient(request)

  // Refresh session if expired - required for Server Components
  const {
    data: { session },
  } = await supabase.auth.getSession()

  // Protect dashboard routes
  if (
    request.nextUrl.pathname.startsWith("/dashboard") ||
    request.nextUrl.pathname.startsWith("/chat") ||
    request.nextUrl.pathname.startsWith("/agents") ||
    request.nextUrl.pathname.startsWith("/code") ||
    request.nextUrl.pathname.startsWith("/workflows") ||
    request.nextUrl.pathname.startsWith("/orchestrate") ||
    request.nextUrl.pathname.startsWith("/automation") ||
    request.nextUrl.pathname.startsWith("/knowledge") ||
    request.nextUrl.pathname.startsWith("/settings")
  ) {
    if (!session) {
      // Redirect to login if not authenticated
      const redirectUrl = request.nextUrl.clone()
      redirectUrl.pathname = "/auth/login"
      redirectUrl.searchParams.set("redirectedFrom", request.nextUrl.pathname)
      return NextResponse.redirect(redirectUrl)
    }
  }

  return response
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     * - api routes (handled separately)
     */
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
}
