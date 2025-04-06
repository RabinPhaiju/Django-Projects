// src/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;

  // Define protected routes
  const protectedRoutes = ['/dashboard'];

  // Check if the current route is protected
  if (protectedRoutes.includes(request.nextUrl.pathname)) {
    if (!token) {
      // Redirect to login page if not authenticated
      return NextResponse.redirect(new URL('/login', request.url));
    }

    // Optionally, validate the token on the server side
    try {
      const isValidToken = await validateToken(token);
      if (!isValidToken) {
        return NextResponse.redirect(new URL('/login', request.url));
      }
    } catch (error) {
      console.error('Token validation failed:', error);
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  // If authenticated or not a protected route, continue
  return NextResponse.next();
}

// Helper function to validate the token (example)
async function validateToken(token: string): Promise<boolean> {
  // Replace this with your actual token validation logic (e.g., call an API or verify JWT signature)
  return true; // Assume token is valid for now
}

export const config = {
  matcher: ['/dashboard'], // Apply middleware only to these routes
};