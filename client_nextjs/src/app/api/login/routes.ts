// src/app/api/login/route.ts
import { serialize } from 'cookie'; // Import serialize from 'cookie'
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const { username, password } = await request.json();

  // Replace this with your actual authentication logic
  if (username === 'admin' && password === 'password') {
    const token = 'your-jwt-token'; // Generate JWT or use a real token

    // Set HTTP-only cookie
    const cookie = serialize('token', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production', // Use HTTPS in production
      maxAge: 60 * 60 * 24, // 1 day
      path: '/',
    });

    return new Response(JSON.stringify({ message: 'Login successful' }), {
      status: 200,
      headers: { 'Set-Cookie': cookie },
    });
  }

  return NextResponse.json({ message: 'Invalid credentials' }, { status: 401 });
}
