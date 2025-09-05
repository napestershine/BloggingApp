'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { User } from '@/types';
import { authAPI, tokenUtils } from '@/lib/api';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (credentials: { username: string; password: string }) => Promise<void>;
  logout: () => void;
  register: (userData: { username: string; email: string; password: string }) => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      if (tokenUtils.isAuthenticated()) {
        const profile = await authAPI.getProfile();
        setUser(profile);
      }
    } catch (error) {
      tokenUtils.removeToken();
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (credentials: { username: string; password: string }) => {
    const authResponse = await authAPI.login(credentials);
    tokenUtils.setToken(authResponse.access_token);
    setUser(authResponse.user);
  };

  const logout = () => {
    tokenUtils.removeToken();
    setUser(null);
  };

  const register = async (userData: { username: string; email: string; password: string }) => {
    const newUser = await authAPI.register(userData);
    setUser(newUser);
  };

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    logout,
    register,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}