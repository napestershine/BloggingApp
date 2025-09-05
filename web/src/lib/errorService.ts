import toast from 'react-hot-toast';

/**
 * Error types for categorizing different kinds of errors
 */
export enum ErrorType {
  NETWORK = 'NETWORK',
  AUTHENTICATION = 'AUTHENTICATION',
  AUTHORIZATION = 'AUTHORIZATION',
  VALIDATION = 'VALIDATION',
  SERVER = 'SERVER',
  CLIENT = 'CLIENT',
  UNKNOWN = 'UNKNOWN',
}

/**
 * Interface for structured error information
 */
export interface ErrorInfo {
  type: ErrorType;
  message: string;
  details?: string;
  statusCode?: number;
  field?: string;
}

/**
 * ErrorService provides comprehensive error handling and user feedback
 * for the BloggingApp NextJS web application.
 * 
 * This service centralizes error handling logic and provides consistent
 * user feedback across the entire application using react-hot-toast.
 * 
 * Features:
 * - HTTP error code handling with user-friendly messages
 * - Network connectivity error detection
 * - Authentication and authorization error handling
 * - Validation error processing with field-specific feedback
 * - Consistent toast notifications with proper styling
 * - Error logging for debugging and monitoring
 * - TypeScript support with proper error typing
 * 
 * Usage:
 * ```typescript
 * // Handle HTTP errors
 * ErrorService.handleHttpError(response);
 * 
 * // Handle fetch errors
 * ErrorService.handleFetchError(error);
 * 
 * // Show custom errors
 * ErrorService.showError('Custom error message');
 * 
 * // Show success messages
 * ErrorService.showSuccess('Operation completed successfully');
 * 
 * // Handle form validation
 * const errors = ErrorService.validateForm(formData, rules);
 * ```
 */
export class ErrorService {
  /**
   * Default error messages for common scenarios
   */
  private static readonly DEFAULT_MESSAGES = {
    NETWORK: 'Please check your internet connection and try again.',
    SERVER: 'Server is temporarily unavailable. Please try again later.',
    AUTHENTICATION: 'Authentication failed. Please check your credentials.',
    AUTHORIZATION: 'You don\'t have permission to perform this action.',
    VALIDATION: 'Please check your input and try again.',
    UNKNOWN: 'Something went wrong. Please try again.',
  };

  /**
   * Toast configuration for consistent styling
   */
  private static readonly TOAST_CONFIG = {
    duration: 4000,
    position: 'top-right' as const,
    style: {
      borderRadius: '8px',
      maxWidth: '500px',
    },
  };

  /**
   * Handles HTTP response errors and shows appropriate user feedback
   * 
   * @param response - Response object from fetch
   * @param customMessage - Optional custom message to override defaults
   * @returns Promise<ErrorInfo> - Structured error information
   * 
   * This method maps HTTP status codes to user-friendly messages:
   * - 400: Bad Request (validation errors)
   * - 401: Unauthorized (authentication required)
   * - 403: Forbidden (insufficient permissions)
   * - 404: Not Found (resource doesn't exist)
   * - 409: Conflict (duplicate data)
   * - 422: Unprocessable Entity (validation errors)
   * - 429: Too Many Requests (rate limiting)
   * - 500+: Server errors
   */
  static async handleHttpError(
    response: Response,
    customMessage?: string
  ): Promise<ErrorInfo> {
    const statusCode = response.status;
    let errorInfo: ErrorInfo;

    try {
      // Try to parse error details from response body
      const errorData = await response.json().catch(() => null);
      const serverMessage = errorData?.detail || errorData?.message;

      // Determine error type and message based on status code
      switch (statusCode) {
        case 400:
        case 422:
          errorInfo = {
            type: ErrorType.VALIDATION,
            message: customMessage || this.parseValidationError(errorData) || this.DEFAULT_MESSAGES.VALIDATION,
            details: serverMessage,
            statusCode,
          };
          break;

        case 401:
          errorInfo = {
            type: ErrorType.AUTHENTICATION,
            message: customMessage || this.DEFAULT_MESSAGES.AUTHENTICATION,
            details: serverMessage,
            statusCode,
          };
          break;

        case 403:
          errorInfo = {
            type: ErrorType.AUTHORIZATION,
            message: customMessage || this.DEFAULT_MESSAGES.AUTHORIZATION,
            details: serverMessage,
            statusCode,
          };
          break;

        case 404:
          errorInfo = {
            type: ErrorType.CLIENT,
            message: customMessage || 'The requested resource was not found.',
            details: serverMessage,
            statusCode,
          };
          break;

        case 409:
          errorInfo = {
            type: ErrorType.VALIDATION,
            message: customMessage || 'This data already exists. Please use different values.',
            details: serverMessage,
            statusCode,
          };
          break;

        case 429:
          errorInfo = {
            type: ErrorType.CLIENT,
            message: customMessage || 'Too many requests. Please wait a moment and try again.',
            details: serverMessage,
            statusCode,
          };
          break;

        case 500:
        case 502:
        case 503:
        case 504:
        default:
          if (statusCode >= 500) {
            errorInfo = {
              type: ErrorType.SERVER,
              message: customMessage || this.DEFAULT_MESSAGES.SERVER,
              details: serverMessage,
              statusCode,
            };
          } else {
            errorInfo = {
              type: ErrorType.UNKNOWN,
              message: customMessage || this.DEFAULT_MESSAGES.UNKNOWN,
              details: serverMessage,
              statusCode,
            };
          }
          break;
      }
    } catch (parseError) {
      // If we can't parse the response, create a generic error
      errorInfo = {
        type: statusCode >= 500 ? ErrorType.SERVER : ErrorType.UNKNOWN,
        message: customMessage || this.DEFAULT_MESSAGES.UNKNOWN,
        statusCode,
      };
    }

    // Log error for debugging
    this.logError('HTTP Error', errorInfo);

    // Show user feedback
    this.showErrorToast(errorInfo.message);

    return errorInfo;
  }

  /**
   * Handles fetch/network errors and provides user feedback
   * 
   * @param error - Error object from fetch operation
   * @param customMessage - Optional custom message to override defaults
   * @returns ErrorInfo - Structured error information
   */
  static handleFetchError(error: unknown, customMessage?: string): ErrorInfo {
    let errorInfo: ErrorInfo;

    if (error instanceof TypeError && error.message.includes('fetch')) {
      // Network connectivity issues
      errorInfo = {
        type: ErrorType.NETWORK,
        message: customMessage || this.DEFAULT_MESSAGES.NETWORK,
        details: error.message,
      };
    } else if (error instanceof Error) {
      // Other JavaScript errors
      errorInfo = {
        type: ErrorType.CLIENT,
        message: customMessage || this.DEFAULT_MESSAGES.UNKNOWN,
        details: error.message,
      };
    } else {
      // Unknown error types
      errorInfo = {
        type: ErrorType.UNKNOWN,
        message: customMessage || this.DEFAULT_MESSAGES.UNKNOWN,
        details: String(error),
      };
    }

    // Log error for debugging
    this.logError('Fetch Error', errorInfo);

    // Show user feedback
    this.showErrorToast(errorInfo.message);

    return errorInfo;
  }

  /**
   * Shows an error toast notification
   * 
   * @param message - Error message to display
   * @param options - Optional toast configuration overrides
   */
  static showError(message: string, options?: Partial<typeof this.TOAST_CONFIG>): void {
    this.showErrorToast(message, options);
  }

  /**
   * Shows a success toast notification
   * 
   * @param message - Success message to display
   * @param options - Optional toast configuration overrides
   */
  static showSuccess(message: string, options?: Partial<typeof this.TOAST_CONFIG>): void {
    toast.success(message, {
      ...this.TOAST_CONFIG,
      ...options,
      duration: options?.duration || 3000, // Shorter duration for success
    });
  }

  /**
   * Shows a warning toast notification
   * 
   * @param message - Warning message to display
   * @param options - Optional toast configuration overrides
   */
  static showWarning(message: string, options?: Partial<typeof this.TOAST_CONFIG>): void {
    toast(message, {
      ...this.TOAST_CONFIG,
      ...options,
      icon: '⚠️',
      style: {
        ...this.TOAST_CONFIG.style,
        backgroundColor: '#f59e0b',
        color: 'white',
        ...options?.style,
      },
    });
  }

  /**
   * Shows an info toast notification
   * 
   * @param message - Info message to display
   * @param options - Optional toast configuration overrides
   */
  static showInfo(message: string, options?: Partial<typeof this.TOAST_CONFIG>): void {
    toast(message, {
      ...this.TOAST_CONFIG,
      ...options,
      icon: 'ℹ️',
      style: {
        ...this.TOAST_CONFIG.style,
        backgroundColor: '#3b82f6',
        color: 'white',
        ...options?.style,
      },
    });
  }

  /**
   * Validates form data against specified rules
   * 
   * @param data - Form data to validate
   * @param rules - Validation rules object
   * @returns Object with field errors or null if valid
   * 
   * Example rules:
   * ```typescript
   * const rules = {
   *   email: ['required', 'email'],
   *   password: ['required', 'min:8'],
   *   username: ['required', 'min:3', 'max:20']
   * };
   * ```
   */
  static validateForm(
    data: Record<string, any>,
    rules: Record<string, string[]>
  ): Record<string, string> | null {
    const errors: Record<string, string> = {};

    for (const [field, fieldRules] of Object.entries(rules)) {
      const value = data[field];
      const error = this.validateField(field, value, fieldRules);
      if (error) {
        errors[field] = error;
      }
    }

    return Object.keys(errors).length > 0 ? errors : null;
  }

  /**
   * Validates a single field against specified rules
   * 
   * @param field - Field name for error messages
   * @param value - Value to validate
   * @param rules - Array of validation rules
   * @returns Error message string or null if valid
   */
  static validateField(field: string, value: any, rules: string[]): string | null {
    const fieldName = field.charAt(0).toUpperCase() + field.slice(1);

    // Required validation
    if (rules.includes('required')) {
      if (value === null || value === undefined || String(value).trim() === '') {
        return `${fieldName} is required.`;
      }
    }

    // Skip other validations if value is empty and not required
    if (!value && !rules.includes('required')) {
      return null;
    }

    const stringValue = String(value).trim();

    // Email validation
    if (rules.includes('email')) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(stringValue)) {
        return 'Please enter a valid email address.';
      }
    }

    // Minimum length validation
    const minRule = rules.find(rule => rule.startsWith('min:'));
    if (minRule) {
      const minLength = parseInt(minRule.split(':')[1]);
      if (stringValue.length < minLength) {
        return `${fieldName} must be at least ${minLength} characters long.`;
      }
    }

    // Maximum length validation
    const maxRule = rules.find(rule => rule.startsWith('max:'));
    if (maxRule) {
      const maxLength = parseInt(maxRule.split(':')[1]);
      if (stringValue.length > maxLength) {
        return `${fieldName} must be no more than ${maxLength} characters long.`;
      }
    }

    // Strong password validation
    if (rules.includes('strong_password')) {
      if (stringValue.length < 8) {
        return 'Password must be at least 8 characters long.';
      }
      if (!/[A-Z]/.test(stringValue)) {
        return 'Password must contain at least one uppercase letter.';
      }
      if (!/[a-z]/.test(stringValue)) {
        return 'Password must contain at least one lowercase letter.';
      }
      if (!/[0-9]/.test(stringValue)) {
        return 'Password must contain at least one number.';
      }
    }

    return null;
  }

  /**
   * Internal method to show error toast with consistent styling
   */
  private static showErrorToast(message: string, options?: Partial<typeof this.TOAST_CONFIG>): void {
    toast.error(message, {
      ...this.TOAST_CONFIG,
      ...options,
    });
  }

  /**
   * Internal method to log errors for debugging
   */
  private static logError(context: string, errorInfo: ErrorInfo): void {
    if (process.env.NODE_ENV === 'development') {
      console.group(`🚨 ${context}`);
      console.error('Type:', errorInfo.type);
      console.error('Message:', errorInfo.message);
      if (errorInfo.details) console.error('Details:', errorInfo.details);
      if (errorInfo.statusCode) console.error('Status Code:', errorInfo.statusCode);
      console.groupEnd();
    }
  }

  /**
   * Internal method to parse validation errors from server response
   */
  private static parseValidationError(errorData: any): string | null {
    if (!errorData) return null;

    // Handle FastAPI validation error format
    if (errorData.detail && Array.isArray(errorData.detail)) {
      const firstError = errorData.detail[0];
      if (firstError?.msg) {
        return firstError.msg;
      }
    }

    // Handle simple string detail
    if (typeof errorData.detail === 'string') {
      return errorData.detail;
    }

    return null;
  }
}