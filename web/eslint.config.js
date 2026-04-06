const js = require('@eslint/js');
const tsPlugin = require('@typescript-eslint/eslint-plugin');
const tsParser = require('@typescript-eslint/parser');

module.exports = [
  // Ignore common build and dependency folders
  {
    ignores: ['node_modules', '.next', 'dist', 'coverage', 'playwright-report', '**/node_modules/**'],
  },

  // Node / tooling configs (not part of the app runtime)
  {
    files: ['*.config.js', '*.config.cjs', 'eslint.config.js', 'postcss.config.js', 'next.config.js', 'tailwind.config.js', 'playwright.config.ts', 'vitest.config.ts'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
      globals: {
        require: 'readonly',
        module: 'readonly',
        process: 'readonly',
        __dirname: 'readonly',
        console: 'readonly',
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
    },
    rules: {
      // allow CommonJS usage in config files
      'no-undef': 'off',
    },
  },

  // Application source files (browser + server)
  {
    files: ['src/**/*.{js,jsx,ts,tsx}', 'middleware.ts', 'src/**'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        ecmaFeatures: { jsx: true },
      },
      globals: {
        React: 'readonly',
        JSX: 'readonly',
        window: 'readonly',
        document: 'readonly',
        localStorage: 'readonly',
        sessionStorage: 'readonly',
        URL: 'readonly',
        URLSearchParams: 'readonly',
        navigator: 'readonly',
        fetch: 'readonly',
        process: 'readonly',
        alert: 'readonly',
        prompt: 'readonly',
        Response: 'readonly',
        Request: 'readonly',
        Headers: 'readonly',
        HTMLElement: 'readonly',
        NodeJS: 'readonly',
        setTimeout: 'readonly',
        clearTimeout: 'readonly',
        setInterval: 'readonly',
        global: 'readonly',
        console: 'readonly',
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
    },
    rules: {
      ...js.configs.recommended.rules,
      // TypeScript handles undefined identifiers more reliably than ESLint here.
      'no-undef': 'off',
      // relax unused vars to avoid blocking CI; prefer fixing code incrementally
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn',
      'prefer-const': 'error',
      'no-console': 'warn',
    },
  },

  // Test files (Jest / Vitest environment)
  {
    files: ['**/__tests__/**', '**/*.test.*', 'src/test/**', 'src/**/test/**', 'src/test/**'],
    languageOptions: {
      parser: tsParser,
      parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
      globals: {
        describe: 'readonly',
        it: 'readonly',
        test: 'readonly',
        expect: 'readonly',
        beforeEach: 'readonly',
        afterEach: 'readonly',
        jest: 'readonly',
        vi: 'readonly',
        global: 'readonly',
        window: 'readonly',
        document: 'readonly',
        fetch: 'readonly',
        process: 'readonly',
      },
    },
    rules: {
      // tests may use console/assertions freely
      'no-undef': 'off',
      '@next/next/no-img-element': 'off'
    },
  },
];
