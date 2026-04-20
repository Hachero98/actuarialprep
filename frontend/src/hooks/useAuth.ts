'use client';

import { useAuthStore } from '@/lib/store';
import { User, AuthTokens } from '@/types';

export function useAuth() {
  const {
    user,
    accessToken,
    refreshToken,
    isLoading,
    error,
    setUser,
    setTokens,
    setLoading,
    setError,
    logout,
  } = useAuthStore();

  const isAuthenticated = !!accessToken;

  const setAuthData = (userData: User, tokens: AuthTokens) => {
    setUser(userData);
    setTokens(tokens);
    localStorage.setItem('accessToken', tokens.accessToken);
    localStorage.setItem('refreshToken', tokens.refreshToken);
  };

  const clearAuthData = () => {
    logout();
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  };

  return {
    user,
    accessToken,
    refreshToken,
    isLoading,
    error,
    isAuthenticated,
    setUser,
    setTokens: setAuthData,
    setLoading,
    setError,
    logout: clearAuthData,
  };
}
