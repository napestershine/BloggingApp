'use client';

import { useTheme } from '@/components/ThemeProvider';
import { useState } from 'react';

/**
 * Props for ThemeToggleButton component
 */
interface ThemeToggleButtonProps {
  /** Optional callback when theme changes */
  onThemeChanged?: () => void;
  /** Size of the icon button (default: 24) */
  size?: number;
  /** Whether to show tooltip on hover (default: true) */
  showTooltip?: boolean;
  /** Custom CSS classes */
  className?: string;
}

/**
 * ThemeToggleButton provides a user interface for switching between
 * light, dark, and system theme modes in the NextJS application.
 * 
 * This component creates an intuitive toggle button that cycles through
 * theme modes and provides visual feedback about the current selection.
 * It integrates seamlessly with the ThemeProvider to persist user preferences.
 * 
 * Features:
 * - Visual icon representation of current theme mode
 * - Smooth animations between theme changes
 * - Tooltip showing current theme mode and next action
 * - Accessibility support with ARIA labels
 * - Consistent styling that adapts to current theme
 * - Loading state handling during theme transitions
 * 
 * The button cycles through modes in this order:
 * System → Light → Dark → System
 * 
 * Usage:
 * ```tsx
 * // In navigation bar
 * <nav>
 *   <ThemeToggleButton />
 * </nav>
 * 
 * // In settings with custom styling
 * <ThemeToggleButton 
 *   className="ml-4 p-2"
 *   onThemeChanged={() => console.log('Theme changed')}
 * />
 * ```
 */
export function ThemeToggleButton({
  onThemeChanged,
  size = 24,
  showTooltip = true,
  className = '',
}: ThemeToggleButtonProps) {
  const { mode, isDark, toggleTheme, displayName, isLoading } = useTheme();
  const [isToggling, setIsToggling] = useState(false);

  /**
   * Get the appropriate icon for the current theme mode
   */
  const getIcon = () => {
    switch (mode) {
      case 'light':
        return (
          <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="transition-transform duration-300"
          >
            <circle cx="12" cy="12" r="5" />
            <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
          </svg>
        );
      case 'dark':
        return (
          <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="transition-transform duration-300"
          >
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
          </svg>
        );
      case 'system':
        return (
          <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="transition-transform duration-300"
          >
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
            <line x1="8" y1="21" x2="16" y2="21" />
            <line x1="12" y1="17" x2="12" y2="21" />
          </svg>
        );
      default:
        return null;
    }
  };

  /**
   * Get tooltip text based on current theme mode
   */
  const getTooltipText = () => {
    switch (mode) {
      case 'system':
        return 'Current: System Default\\nClick to switch to Light Mode';
      case 'light':
        return 'Current: Light Mode\\nClick to switch to Dark Mode';
      case 'dark':
        return 'Current: Dark Mode\\nClick to switch to System Default';
      default:
        return 'Toggle theme';
    }
  };

  /**
   * Handle theme toggle with user feedback
   */
  const handleToggle = async () => {
    if (isLoading || isToggling) return;

    try {
      setIsToggling(true);
      await new Promise(resolve => setTimeout(resolve, 100)); // Brief delay for UX
      toggleTheme();
      onThemeChanged?.();
    } catch (error) {
      console.error('Error toggling theme:', error);
    } finally {
      setIsToggling(false);
    }
  };

  return (
    <button
      onClick={handleToggle}
      disabled={isLoading || isToggling}
      title={showTooltip ? getTooltipText() : undefined}
      aria-label={`Switch theme. Current: ${displayName}`}
      className={`
        inline-flex items-center justify-center
        p-2 rounded-lg
        transition-all duration-200 ease-in-out
        hover:bg-gray-100 dark:hover:bg-gray-800
        focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
        disabled:opacity-50 disabled:cursor-not-allowed
        dark:focus:ring-offset-gray-900
        ${isDark ? 'text-gray-300 hover:text-white' : 'text-gray-700 hover:text-black'}
        ${className}
      `}
    >
      <div
        className={`
          transition-transform duration-300 ease-in-out
          ${isToggling ? 'rotate-180 scale-110' : 'rotate-0 scale-100'}
        `}
      >
        {getIcon()}
      </div>
    </button>
  );
}

/**
 * Props for ThemeSelector component
 */
interface ThemeSelectorProps {
  /** Optional callback when theme changes */
  onThemeChanged?: () => void;
  /** Whether to show labels next to options (default: true) */
  showLabels?: boolean;
  /** Custom CSS classes */
  className?: string;
}

/**
 * ThemeSelector provides a comprehensive theme selection interface
 * with radio buttons for each theme mode.
 * 
 * This component is ideal for settings screens where users need
 * explicit control over theme selection with clear visual indicators.
 * 
 * Features:
 * - Radio button interface for clear selection
 * - Visual icons for each theme mode
 * - Detailed descriptions for each option
 * - Accessibility support with proper labeling
 * - Responsive design that adapts to container
 * 
 * Usage:
 * ```tsx
 * // In settings page
 * <div className="settings-section">
 *   <h3>Appearance</h3>
 *   <ThemeSelector onThemeChanged={() => saveSettings()} />
 * </div>
 * 
 * // Compact version without labels
 * <ThemeSelector showLabels={false} className="flex-row space-x-4" />
 * ```
 */
export function ThemeSelector({
  onThemeChanged,
  showLabels = true,
  className = '',
}: ThemeSelectorProps) {
  const { mode, setMode, isLoading } = useTheme();

  const options = [
    {
      value: 'system' as const,
      label: 'System Default',
      description: 'Follow your device setting',
      icon: (
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
          <line x1="8" y1="21" x2="16" y2="21" />
          <line x1="12" y1="17" x2="12" y2="21" />
        </svg>
      ),
    },
    {
      value: 'light' as const,
      label: 'Light Mode',
      description: 'Always use light theme',
      icon: (
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="12" cy="12" r="5" />
          <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
        </svg>
      ),
    },
    {
      value: 'dark' as const,
      label: 'Dark Mode',
      description: 'Always use dark theme',
      icon: (
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
      ),
    },
  ];

  const handleChange = (newMode: 'light' | 'dark' | 'system') => {
    if (isLoading) return;
    setMode(newMode);
    onThemeChanged?.();
  };

  return (
    <div className={`space-y-3 ${className}`}>
      {showLabels && (
        <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100">
          Theme Mode
        </h4>
      )}
      <div className="space-y-2">
        {options.map((option) => (
          <label
            key={option.value}
            className={`
              flex items-center p-3 rounded-lg border cursor-pointer
              transition-all duration-200
              ${mode === option.value
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-400'
                : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
              }
              ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}
            `}
          >
            <input
              type="radio"
              name="theme"
              value={option.value}
              checked={mode === option.value}
              onChange={() => handleChange(option.value)}
              disabled={isLoading}
              className="sr-only"
            />
            <div className="flex items-center space-x-3 w-full">
              <div
                className={`
                  flex-shrink-0
                  ${mode === option.value
                    ? 'text-blue-600 dark:text-blue-400'
                    : 'text-gray-400 dark:text-gray-500'
                  }
                `}
              >
                {option.icon}
              </div>
              {showLabels && (
                <div className="flex-1 min-w-0">
                  <p
                    className={`
                      text-sm font-medium
                      ${mode === option.value
                        ? 'text-blue-900 dark:text-blue-100'
                        : 'text-gray-900 dark:text-gray-100'
                      }
                    `}
                  >
                    {option.label}
                  </p>
                  <p
                    className={`
                      text-xs
                      ${mode === option.value
                        ? 'text-blue-600 dark:text-blue-300'
                        : 'text-gray-500 dark:text-gray-400'
                      }
                    `}
                  >
                    {option.description}
                  </p>
                </div>
              )}
              <div
                className={`
                  w-4 h-4 border-2 rounded-full flex-shrink-0
                  ${mode === option.value
                    ? 'border-blue-600 dark:border-blue-400'
                    : 'border-gray-300 dark:border-gray-600'
                  }
                `}
              >
                {mode === option.value && (
                  <div className="w-2 h-2 bg-blue-600 dark:bg-blue-400 rounded-full m-auto mt-[1px]" />
                )}
              </div>
            </div>
          </label>
        ))}
      </div>
    </div>
  );
}