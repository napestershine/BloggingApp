import { NextRequest, NextResponse } from 'next/server';
import { jwtDecode } from 'jwt-decode';

interface TokenPayload {
  sub: string; // username
  exp: number;
  iat: number;
}

// Helper to check if request is from mobile device
function isMobileUserAgent(userAgent: string): boolean {
  const mobileKeywords = [
    'mobile', 'android', 'iphone', 'ipad', 'ipod', 
    'blackberry', 'windows phone', 'webos', 'tablet'
  ];
  return mobileKeywords.some(keyword => userAgent.toLowerCase().includes(keyword));
}

// Helper to check if request is from desktop based on user agent and viewport
function isDesktopRequest(request: NextRequest): boolean {
  const userAgent = request.headers.get('user-agent') || '';
  
  // If it's a mobile user agent, it's not desktop
  if (isMobileUserAgent(userAgent)) {
    return false;
  }
  
  // Check for desktop indicators
  const desktopKeywords = ['windows', 'macintosh', 'linux'];
  return desktopKeywords.some(keyword => userAgent.toLowerCase().includes(keyword));
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Check if the request is for admin routes
  if (pathname.startsWith('/admin')) {
    
    // Block mobile access to admin
    if (!isDesktopRequest(request)) {
      return NextResponse.redirect(new URL('/admin/mobile-blocked', request.url));
    }
    
    // Check authentication for admin routes
    const token = request.cookies.get('access_token')?.value || 
                  request.headers.get('authorization')?.replace('Bearer ', '');
    
    if (!token) {
      // Redirect to login if not authenticated
      const loginUrl = new URL('/auth/login', request.url);
      loginUrl.searchParams.set('redirect', pathname);
      return NextResponse.redirect(loginUrl);
    }
    
    try {
      // Decode token to check if it's valid and not expired
      const decoded = jwtDecode<TokenPayload>(token);
      const currentTime = Math.floor(Date.now() / 1000);
      
      if (decoded.exp < currentTime) {
        // Token expired
        const loginUrl = new URL('/auth/login', request.url);
        loginUrl.searchParams.set('redirect', pathname);
        loginUrl.searchParams.set('expired', 'true');
        return NextResponse.redirect(loginUrl);
      }
      
      // Token is valid, allow the request to continue
      // The actual role checking will be done client-side and server-side in API calls
      return NextResponse.next();
      
    } catch (error) {
      // Invalid token
      const loginUrl = new URL('/auth/login', request.url);
      loginUrl.searchParams.set('redirect', pathname);
      loginUrl.searchParams.set('invalid', 'true');
      return NextResponse.redirect(loginUrl);
    }
  }
  
  // For non-admin routes, just continue
  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder files
     */
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|css|js|mjs|ts|tsx|json|map|woff|woff2|ttf|eot|otf|ico)$).*)',
  ],
};