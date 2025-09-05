'use client';

import { createContext, useContext, useEffect, useState } from 'react';

/**
 * Theme modes supported by the application
 * - light: Force light theme
 * - dark: Force dark theme
 * - system: Follow system preference
 */
export type ThemeMode = 'light' | 'dark' | 'system';

/**
 * Theme context interface providing theme state and controls
 */
interface ThemeContextType {
  /** Current theme mode setting */
  mode: ThemeMode;
  /** Computed theme based on mode and system preference */
  theme: 'light' | 'dark';
  /** Whether the theme is currently dark */
  isDark: boolean;
  /** Loading state for theme operations */
  isLoading: boolean;
  /** Set specific theme mode */
  setMode: (mode: ThemeMode) => void;
  /** Toggle between light and dark modes */
  toggleTheme: () => void;
  /** User-friendly display name for current mode */
  displayName: string;
}

/**
 * Theme context for accessing theme state throughout the application
 */
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

/**
 * ThemeProvider manages application theming with support for:
 * - Light and dark theme modes
 * - System preference detection
 * - Persistent theme storage
 * - Real-time theme switching
 * 
 * Key Features:
 * - Automatic system theme detection using prefers-color-scheme
 * - LocalStorage persistence for user preferences
 * - Smooth theme transitions with CSS classes
 * - SSR-safe theme loading to prevent hydration issues
 * - Comprehensive error handling for edge cases
 * 
 * Example Usage:
 * ```tsx
 * // Wrap your app
 * <ThemeProvider>
 *   <MyApp />
 * </ThemeProvider>
 * 
 * // Use in components
 * const { isDark, toggleTheme, setMode } = useTheme();
 * ```
 */
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  // State management for theme mode and computed values
  const [mode, setModeState] = useState<ThemeMode>('system');
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Initialize theme on component mount
   * Loads saved preference and sets up system preference listeners
   */
  useEffect(() => {
    initializeTheme();
  }, []);

  /**
   * Update computed theme when mode changes or system preference changes
   */
  useEffect(() => {
    updateComputedTheme();
  }, [mode]);

  /**
   * Initialize theme system with error handling
   * Loads from localStorage and sets up system preference monitoring
   */
  const initializeTheme = async () => {
    try {
      setIsLoading(true);
      
      // Load saved theme preference from localStorage
      const savedMode = localStorage.getItem('theme-mode') as ThemeMode;
      if (savedMode && ['light', 'dark', 'system'].includes(savedMode)) {
        setModeState(savedMode);
      } else {
        // Default to system preference if no saved setting
        setModeState('system');
      }

      // Set up system preference change listener
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleSystemThemeChange = () => {
        if (mode === 'system') {
          updateComputedTheme();
        }
      };

      // Modern browsers support addEventListener
      if (mediaQuery.addEventListener) {
        mediaQuery.addEventListener('change', handleSystemThemeChange);
      } else {
        // Fallback for older browsers
        mediaQuery.addListener(handleSystemThemeChange);
      }

      // Cleanup function for removing listeners
      return () => {
        if (mediaQuery.removeEventListener) {
          mediaQuery.removeEventListener('change', handleSystemThemeChange);
        } else {
          mediaQuery.removeListener(handleSystemThemeChange);
        }
      };
    } catch (error) {
      console.error('Error initializing theme:', error);
      // Fallback to light theme on error
      setModeState('light');
      setTheme('light');
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Update computed theme based on current mode and system preference
   * Applies CSS classes and localStorage updates
   */
  const updateComputedTheme = () => {
    try {
      let computedTheme: 'light' | 'dark';

      if (mode === 'system') {
        // Use system preference for 'system' mode
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        computedTheme = prefersDark ? 'dark' : 'light';
      } else {
        // Use explicit mode setting
        computedTheme = mode as 'light' | 'dark';
      }

      // Update state
      setTheme(computedTheme);

      // Apply CSS classes for styling
      const root = document.documentElement;
      root.classList.remove('light', 'dark');
      root.classList.add(computedTheme);

      // Apply data attribute for CSS selectors
      root.setAttribute('data-theme', computedTheme);

      // Update Tailwind dark mode class
      if (computedTheme === 'dark') {
        root.classList.add('dark');
      } else {
        root.classList.remove('dark');
      }
    } catch (error) {
      console.error('Error updating computed theme:', error);
    }
  };

  /**
   * Set theme mode with persistence and validation
   * 
   * @param newMode - The theme mode to set
   */
  const setMode = (newMode: ThemeMode) => {
    try {
      // Validate input
      if (!['light', 'dark', 'system'].includes(newMode)) {
        console.error('Invalid theme mode:', newMode);
        return;
      }

      setModeState(newMode);
      
      // Persist to localStorage
      localStorage.setItem('theme-mode', newMode);
    } catch (error) {
      console.error('Error setting theme mode:', error);
    }
  };

  /**
   * Toggle between light and dark themes
   * If currently in system mode, switches to opposite of current system setting
   */
  const toggleTheme = () => {
    try {
      let newMode: ThemeMode;

      switch (mode) {
        case 'light':
          newMode = 'dark';
          break;
        case 'dark':
          newMode = 'light';
          break;
        case 'system':
          // Toggle to opposite of current system setting
          const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
          newMode = prefersDark ? 'light' : 'dark';
          break;
        default:
          newMode = 'light';
      }

      setMode(newMode);
    } catch (error) {
      console.error('Error toggling theme:', error);
    }
  };

  /**
   * Get user-friendly display name for current theme mode
   */
  const getDisplayName = (): string => {
    switch (mode) {
      case 'light':
        return 'Light Mode';
      case 'dark':
        return 'Dark Mode';
      case 'system':
        return 'System Default';
      default:
        return 'Light Mode';
    }
  };

  // Context value with all theme state and controls
  const value: ThemeContextType = {
    mode,
    theme,
    isDark: theme === 'dark',
    isLoading,
    setMode,
    toggleTheme,
    displayName: getDisplayName(),
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

/**
 * Hook for accessing theme context
 * 
 * @returns Theme context with state and controls
 * @throws Error if used outside ThemeProvider
 * 
 * Example Usage:
 * ```tsx
 * function MyComponent() {
 *   const { isDark, toggleTheme, mode, setMode } = useTheme();
 *   
 *   return (
 *     <div>
 *       <p>Current theme: {isDark ? 'Dark' : 'Light'}</p>
 *       <button onClick={toggleTheme}>
 *         Toggle Theme
 *       </button>
 *       <select 
 *         value={mode} 
 *         onChange={(e) => setMode(e.target.value as ThemeMode)}
 *       >
 *         <option value="light">Light</option>
 *         <option value="dark">Dark</option>
 *         <option value="system">System</option>
 *       </select>
 *     </div>
 *   );
 * }
 * ```
 */
export function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}

/**
 * Higher-order component for wrapping components with theme context
 * Useful for testing or conditional theme provision
 */
export function withTheme<P extends object>(
  Component: React.ComponentType<P>
): React.ComponentType<P> {
  return function ThemedComponent(props: P) {
    return (
      <ThemeProvider>
        <Component {...props} />
      </ThemeProvider>
    );
  };
}