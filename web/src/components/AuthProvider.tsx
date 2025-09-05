'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { User } from '@/types';
import { authAPI, tokenUtils } from '@/lib/api';
import { ErrorService } from '@/lib/errorService';

/**
 * Authentication context interface providing auth state and methods
 */
interface AuthContextType {
  /** Current authenticated user */
  user: User | null;
  /** Loading state for auth operations */
  isLoading: boolean;
  /** Whether user is authenticated */
  isAuthenticated: boolean;
  /** Login with credentials */
  login: (credentials: { username: string; password: string }) => Promise<boolean>;
  /** Logout current user */
  logout: () => void;
  /** Register new user */
  register: (userData: { username: string; email: string; password: string; name: string }) => Promise<boolean>;
  /** Refresh authentication state */
  refresh: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

/**
 * AuthProvider manages user authentication state and provides authentication
 * functionality throughout the BloggingApp NextJS application.
 * 
 * This provider offers comprehensive authentication features including:
 * - JWT token-based authentication with secure storage
 * - Automatic token validation and refresh
 * - User registration and login with error handling
 * - Persistent authentication state across page refreshes
 * - Integration with ErrorService for user-friendly feedback
 * 
 * Key Features:
 * - Secure token management with automatic cleanup
 * - Real-time authentication state updates
 * - Comprehensive error handling with user feedback
 * - Loading states for all auth operations
 * - Automatic logout on token expiration
 * 
 * Example Usage:
 * ```tsx
 * function LoginForm() {
 *   const { login, isLoading } = useAuth();
 *   
 *   const handleSubmit = async (credentials) => {
 *     const success = await login(credentials);
 *     if (success) {
 *       router.push('/dashboard');
 *     }
 *   };
 * }
 * ```
 */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  /**
   * Check current authentication status and load user data
   * Called on app initialization and manual refresh
   */
  const checkAuth = async () => {
    try {
      if (tokenUtils.isAuthenticated()) {
        const profile = await authAPI.getProfile();
        setUser(profile);
      }
    } catch (error) {
      // Token is invalid or expired, clean up
      tokenUtils.removeToken();
      setUser(null);
      
      // Only show error if it's not a simple token expiration
      if (error instanceof Response && error.status !== 401) {
        ErrorService.handleHttpError(error, 'Failed to verify authentication');
      }
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Authenticate user with username and password
   * 
   * @param credentials - User login credentials
   * @returns Promise<boolean> - Success status
   */
  const login = async (credentials: { username: string; password: string }): Promise<boolean> => {
    try {
      setIsLoading(true);
      
      // Validate credentials
      const errors = ErrorService.validateForm(credentials, {
        username: ['required', 'min:3'],
        password: ['required'],
      });
      
      if (errors) {
        const firstError = Object.values(errors)[0];
        ErrorService.showError(firstError);
        return false;
      }

      const authResponse = await authAPI.login(credentials);
      
      // Store token and user data
      tokenUtils.setToken(authResponse.access_token);
      setUser(authResponse.user);
      
      ErrorService.showSuccess('Login successful!');
      return true;
      
    } catch (error) {
      if (error instanceof Response) {
        await ErrorService.handleHttpError(error, 'Login failed');
      } else {
        ErrorService.handleFetchError(error, 'Login failed. Please try again.');
      }
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Register new user account
   * 
   * @param userData - New user registration data
   * @returns Promise<boolean> - Success status
   */
  const register = async (userData: { 
    username: string; 
    email: string; 
    password: string; 
    name: string;
  }): Promise<boolean> => {
    try {
      setIsLoading(true);
      
      // Validate registration data
      const errors = ErrorService.validateForm(userData, {
        username: ['required', 'min:3', 'max:20'],
        email: ['required', 'email'],
        password: ['required', 'min:8', 'strong_password'],
        name: ['required', 'min:2'],
      });
      
      if (errors) {
        const firstError = Object.values(errors)[0];
        ErrorService.showError(firstError);
        return false;
      }

      const newUser = await authAPI.register(userData);
      
      // Auto-login after successful registration
      const loginSuccess = await login({
        username: userData.username,
        password: userData.password,
      });
      
      if (loginSuccess) {
        ErrorService.showSuccess('Registration successful! Welcome to BloggingApp.');
      }
      
      return loginSuccess;
      
    } catch (error) {
      if (error instanceof Response) {
        await ErrorService.handleHttpError(error, 'Registration failed');
      } else {
        ErrorService.handleFetchError(error, 'Registration failed. Please try again.');
      }
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Logout current user and clean up authentication state
   */
  const logout = () => {
    try {
      tokenUtils.removeToken();
      setUser(null);
      ErrorService.showInfo('You have been logged out.');
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear state even if there's an error
      tokenUtils.removeToken();
      setUser(null);
    }
  };

  /**
   * Manually refresh authentication state
   * Useful after token updates or user profile changes
   */
  const refresh = async (): Promise<void> => {
    setIsLoading(true);
    await checkAuth();
  };

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    logout,
    register,
    refresh,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook for accessing authentication context
 * 
 * @returns Authentication context with state and methods
 * @throws Error if used outside AuthProvider
 * 
 * Example Usage:
 * ```tsx
 * function ProfilePage() {
 *   const { user, isAuthenticated, logout } = useAuth();
 *   
 *   if (!isAuthenticated) {
 *     return <LoginForm />;
 *   }
 *   
 *   return (
 *     <div>
 *       <h1>Welcome, {user.name}!</h1>
 *       <button onClick={logout}>Logout</button>
 *     </div>
 *   );
 * }
 * ```
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}