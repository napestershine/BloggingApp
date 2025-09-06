import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';

import '../services/auth_service.dart';
import '../services/error_service.dart';
import '../utils/responsive_layout.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _retypedPasswordController = TextEditingController();
  
  bool _isLoginMode = true;
  bool _obscurePassword = true;
  bool _obscureRetypedPassword = true;

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    _nameController.dispose();
    _emailController.dispose();
    _retypedPasswordController.dispose();
    super.dispose();
  }

  /// Handles form submission for both login and registration
  /// 
  /// This method performs comprehensive validation and error handling:
  /// 1. Validates form fields using Flutter's built-in validation
  /// 2. Calls appropriate authentication service method
  /// 3. Provides user feedback through error service
  /// 4. Navigates to main app on success
  /// 
  /// Error scenarios handled:
  /// - Network connectivity issues
  /// - Invalid credentials
  /// - Server errors
  /// - Validation failures
  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    final authService = Provider.of<AuthService>(context, listen: false);
    
    try {
      bool success;
      if (_isLoginMode) {
        // Perform login with input validation
        final username = _usernameController.text.trim();
        final password = _passwordController.text;
        
        if (username.isEmpty || password.isEmpty) {
          ErrorService.showError(context, 'Please fill in all required fields');
          return;
        }
        
        success = await authService.login(username, password);
      } else {
        // Perform registration with comprehensive validation
        final username = _usernameController.text.trim();
        final password = _passwordController.text;
        final retypedPassword = _retypedPasswordController.text;
        final name = _nameController.text.trim();
        final email = _emailController.text.trim();
        
        // Additional password validation
        if (password != retypedPassword) {
          ErrorService.showError(context, 'Passwords do not match');
          return;
        }
        
        success = await authService.register(
          username, password, retypedPassword, name, email,
        );
      }

      if (success && mounted) {
        // Success - navigate to main app
        ErrorService.showSuccess(
          context, 
          _isLoginMode ? 'Login successful!' : 'Registration successful!',
        );
        context.go('/blogs');
      } else if (mounted) {
        // Authentication failed - show appropriate error
        final errorMessage = _isLoginMode 
            ? 'Login failed. Please check your credentials and try again.'
            : 'Registration failed. Please check your information and try again.';
        ErrorService.showError(context, errorMessage);
      }
    } catch (e) {
      // Handle unexpected errors
      if (mounted) {
        ErrorService.handleException(
          context, 
          e,
          customMessage: _isLoginMode 
              ? 'Login error occurred. Please try again.'
              : 'Registration error occurred. Please try again.',
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_isLoginMode ? 'Login' : 'Register'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: ResponsiveWidth.centered(
        context,
        SingleChildScrollView(
          padding: ResponsivePadding.page(context),
          child: ResponsiveLayout(
            mobile: _buildMobileLayout(),
            tablet: _buildTabletLayout(),
          ),
        ),
      ),
    );
  }

  Widget _buildMobileLayout() {
    return _buildForm();
  }

  Widget _buildTabletLayout() {
    return Row(
      children: [
        Expanded(
          child: Card(
            elevation: 8,
            child: Container(
              padding: const EdgeInsets.all(40),
              constraints: const BoxConstraints(maxWidth: 500),
              child: _buildForm(),
            ),
          ),
        ),
        const SizedBox(width: 40),
        Expanded(
          child: _buildWelcomeSection(),
        ),
      ],
    );
  }

  Widget _buildWelcomeSection() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(
          Icons.article,
          size: 120,
          color: Theme.of(context).colorScheme.primary,
        ),
        const SizedBox(height: 24),
        Text(
          'Welcome to SF5 Blog',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        Text(
          'Create, share, and discover amazing blog posts from writers around the world.',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
          ),
        ),
      ],
    );
  }

  Widget _buildForm() {
    return Form(
      key: _formKey,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (ResponsiveBreakpoints.isMobile(context)) ...[
            Icon(
              Icons.article,
              size: 80,
              color: Theme.of(context).colorScheme.primary,
            ),
            const SizedBox(height: 32),
          ],
              
              TextFormField(
                controller: _usernameController,
                decoration: const InputDecoration(
                  labelText: 'Username',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.person),
                ),
                validator: (value) {
                  return ErrorService.validateField(
                    'Username', 
                    value, 
                    ['required', 'min:3']
                  );
                },
              ),
              const SizedBox(height: 16),
              
              if (!_isLoginMode) ...[
                TextFormField(
                  controller: _nameController,
                  decoration: const InputDecoration(
                    labelText: 'Full Name',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.badge),
                  ),
                  validator: (value) {
                    return ErrorService.validateField(
                      'Full name', 
                      value, 
                      ['required', 'min:2']
                    );
                  },
                ),
                const SizedBox(height: 16),
                
                TextFormField(
                  controller: _emailController,
                  decoration: const InputDecoration(
                    labelText: 'Email',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.email),
                  ),
                  keyboardType: TextInputType.emailAddress,
                  validator: (value) {
                    return ErrorService.validateField(
                      'Email', 
                      value, 
                      ['required', 'email']
                    );
                  },
                ),
                const SizedBox(height: 16),
              ],
              
              TextFormField(
                controller: _passwordController,
                decoration: InputDecoration(
                  labelText: 'Password',
                  border: const OutlineInputBorder(),
                  prefixIcon: const Icon(Icons.lock),
                  suffixIcon: IconButton(
                    icon: Icon(_obscurePassword ? Icons.visibility : Icons.visibility_off),
                    onPressed: () {
                      setState(() {
                        _obscurePassword = !_obscurePassword;
                      });
                    },
                  ),
                ),
                obscureText: _obscurePassword,
                validator: (value) {
                  if (_isLoginMode) {
                    return ErrorService.validateField(
                      'Password', 
                      value, 
                      ['required']
                    );
                  } else {
                    return ErrorService.validateField(
                      'Password', 
                      value, 
                      ['required', 'min:8', 'strong_password']
                    );
                  }
                },
              ),
              const SizedBox(height: 16),
              
              if (!_isLoginMode) ...[
                TextFormField(
                  controller: _retypedPasswordController,
                  decoration: InputDecoration(
                    labelText: 'Confirm Password',
                    border: const OutlineInputBorder(),
                    prefixIcon: const Icon(Icons.lock_outline),
                    suffixIcon: IconButton(
                      icon: Icon(_obscureRetypedPassword ? Icons.visibility : Icons.visibility_off),
                      onPressed: () {
                        setState(() {
                          _obscureRetypedPassword = !_obscureRetypedPassword;
                        });
                      },
                    ),
                  ),
                  obscureText: _obscureRetypedPassword,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please confirm your password';
                    }
                    if (value != _passwordController.text) {
                      return 'Passwords do not match';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 24),
              ] else
                const SizedBox(height: 24),
              
              Consumer<AuthService>(
                builder: (context, authService, child) {
                  return SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: authService.isLoading ? null : _submit,
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                      ),
                      child: authService.isLoading
                          ? const CircularProgressIndicator()
                          : Text(_isLoginMode ? 'Login' : 'Register'),
                    ),
                  );
                },
              ),
              const SizedBox(height: 16),
              
              TextButton(
                onPressed: () {
                  setState(() {
                    _isLoginMode = !_isLoginMode;
                  });
                },
                child: Text(
                  _isLoginMode
                      ? 'Don\'t have an account? Register'
                      : 'Already have an account? Login',
                ),
              ),
              
              if (_isLoginMode) ...[
                const SizedBox(height: 8),
                TextButton(
                  onPressed: () {
                    context.push('/password-reset');
                  },
                  child: const Text('Forgot Password?'),
                ),
              ],
            ],
          ),
        );
      }
    );
  }
}