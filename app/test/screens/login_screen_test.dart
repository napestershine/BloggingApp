import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:provider/provider.dart';
import 'package:sf5_blog_app/screens/login_screen.dart';
import 'package:sf5_blog_app/services/auth_service.dart';

import 'login_screen_test.mocks.dart';

@GenerateMocks([AuthService])
void main() {
  group('LoginScreen Widget Tests', () {
    late MockAuthService mockAuthService;

    setUp(() {
      mockAuthService = MockAuthService();
      
      // Default mock behavior
      when(mockAuthService.isLoading).thenReturn(false);
      when(mockAuthService.isAuthenticated).thenReturn(false);
    });

    Widget createLoginScreen() {
      return MaterialApp(
        home: ChangeNotifierProvider<AuthService>.value(
          value: mockAuthService,
          child: const LoginScreen(),
        ),
      );
    }

    group('UI Elements', () {
      testWidgets('should display login form by default', (WidgetTester tester) async {
        await tester.pumpWidget(createLoginScreen());

        // Check for form fields
        expect(find.byType(TextFormField), findsNWidgets(2)); // Username and password
        expect(find.text('Username'), findsOneWidget);
        expect(find.text('Password'), findsOneWidget);
        
        // Check for login button
        expect(find.text('Login'), findsOneWidget);
        
        // Check for registration link
        expect(find.text("Don't have an account? Register"), findsOneWidget);
      });

      testWidgets('should switch to registration form when tapped', (WidgetTester tester) async {
        await tester.pumpWidget(createLoginScreen());

        // Tap on registration link
        await tester.tap(find.text("Don't have an account? Register"));
        await tester.pumpAndSettle();

        // Check for registration form fields
        expect(find.byType(TextFormField), findsNWidgets(5)); // Username, password, retype, name, email
        expect(find.text('Name'), findsOneWidget);
        expect(find.text('Email'), findsOneWidget);
        expect(find.text('Retype Password'), findsOneWidget);
        
        // Check for register button
        expect(find.text('Register'), findsOneWidget);
        
        // Check for login link
        expect(find.text('Already have an account? Login'), findsOneWidget);
      });

      testWidgets('should show password visibility toggle', (WidgetTester tester) async {
        await tester.pumpWidget(createLoginScreen());

        // Find password field
        final passwordField = find.byKey(const Key('password_field'));
        expect(passwordField, findsOneWidget);

        // Find visibility toggle button
        final visibilityToggle = find.byIcon(Icons.visibility);
        expect(visibilityToggle, findsOneWidget);

        // Tap visibility toggle
        await tester.tap(visibilityToggle);
        await tester.pumpAndSettle();

        // Check icon changed
        expect(find.byIcon(Icons.visibility_off), findsOneWidget);
      });
    });

    group('Form Validation', () {
      testWidgets('should show validation errors for empty fields', (WidgetTester tester) async {
        await tester.pumpWidget(createLoginScreen());

        // Try to submit form without filling fields
        await tester.tap(find.text('Login'));
        await tester.pumpAndSettle();

        // Check for validation messages
        expect(find.text('Please enter your username'), findsOneWidget);
        expect(find.text('Please enter your password'), findsOneWidget);
      });

      testWidgets('should validate password length', (WidgetTester tester) async {
        await tester.pumpWidget(createLoginScreen());

        // Enter short password
        await tester.enterText(find.byKey(const Key('username_field')), 'testuser');
        await tester.enterText(find.byKey(const Key('password_field')), '123');
        
        await tester.tap(find.text('Login'));
        await tester.pumpAndSettle();

        expect(find.text('Password must be at least 6 characters'), findsOneWidget);
      });

      testWidgets('should validate email format in registration', (WidgetTester tester) async {
        await tester.pumpWidget(createLoginScreen());

        // Switch to registration
        await tester.tap(find.text("Don't have an account? Register"));
        await tester.pumpAndSettle();

        // Enter invalid email
        await tester.enterText(find.byKey(const Key('email_field')), 'invalid-email');
        await tester.tap(find.text('Register'));
        await tester.pumpAndSettle();

        expect(find.text('Please enter a valid email address'), findsOneWidget);
      });

      testWidgets('should validate password confirmation in registration', (WidgetTester tester) async {
        await tester.pumpWidget(createLoginScreen());

        // Switch to registration
        await tester.tap(find.text("Don't have an account? Register"));
        await tester.pumpAndSettle();

        // Enter mismatched passwords
        await tester.enterText(find.byKey(const Key('password_field')), 'password123');
        await tester.enterText(find.byKey(const Key('retype_password_field')), 'different123');
        await tester.tap(find.text('Register'));
        await tester.pumpAndSettle();

        expect(find.text('Passwords do not match'), findsOneWidget);
      });
    });

    group('Authentication', () {
      testWidgets('should call login service on form submission', (WidgetTester tester) async {
        when(mockAuthService.login(any, any)).thenAnswer((_) async => true);

        await tester.pumpWidget(createLoginScreen());

        // Fill form
        await tester.enterText(find.byKey(const Key('username_field')), 'testuser');
        await tester.enterText(find.byKey(const Key('password_field')), 'password123');

        // Submit form
        await tester.tap(find.text('Login'));
        await tester.pumpAndSettle();

        // Verify login was called
        verify(mockAuthService.login('testuser', 'password123')).called(1);
      });

      testWidgets('should call register service on registration form submission', (WidgetTester tester) async {
        when(mockAuthService.register(any, any, any, any, any)).thenAnswer((_) async => true);

        await tester.pumpWidget(createLoginScreen());

        // Switch to registration
        await tester.tap(find.text("Don't have an account? Register"));
        await tester.pumpAndSettle();

        // Fill registration form
        await tester.enterText(find.byKey(const Key('username_field')), 'newuser');
        await tester.enterText(find.byKey(const Key('password_field')), 'password123');
        await tester.enterText(find.byKey(const Key('retype_password_field')), 'password123');
        await tester.enterText(find.byKey(const Key('name_field')), 'New User');
        await tester.enterText(find.byKey(const Key('email_field')), 'new@example.com');

        // Submit form
        await tester.tap(find.text('Register'));
        await tester.pumpAndSettle();

        // Verify register was called
        verify(mockAuthService.register(
          'newuser', 'password123', 'password123', 'New User', 'new@example.com'
        )).called(1);
      });

      testWidgets('should show loading indicator during authentication', (WidgetTester tester) async {
        when(mockAuthService.isLoading).thenReturn(true);
        when(mockAuthService.login(any, any)).thenAnswer((_) async => true);

        await tester.pumpWidget(createLoginScreen());

        // Should show loading indicator instead of login button
        expect(find.byType(CircularProgressIndicator), findsOneWidget);
        expect(find.text('Login'), findsNothing);
      });

      testWidgets('should show error message on login failure', (WidgetTester tester) async {
        when(mockAuthService.login(any, any)).thenAnswer((_) async => false);

        await tester.pumpWidget(createLoginScreen());

        // Fill and submit form
        await tester.enterText(find.byKey(const Key('username_field')), 'testuser');
        await tester.enterText(find.byKey(const Key('password_field')), 'wrongpassword');
        await tester.tap(find.text('Login'));
        await tester.pumpAndSettle();

        // Should show error snackbar
        expect(find.text('Login failed. Please check your credentials.'), findsOneWidget);
      });

      testWidgets('should show error message on registration failure', (WidgetTester tester) async {
        when(mockAuthService.register(any, any, any, any, any)).thenAnswer((_) async => false);

        await tester.pumpWidget(createLoginScreen());

        // Switch to registration and fill form
        await tester.tap(find.text("Don't have an account? Register"));
        await tester.pumpAndSettle();

        await tester.enterText(find.byKey(const Key('username_field')), 'existinguser');
        await tester.enterText(find.byKey(const Key('password_field')), 'password123');
        await tester.enterText(find.byKey(const Key('retype_password_field')), 'password123');
        await tester.enterText(find.byKey(const Key('name_field')), 'New User');
        await tester.enterText(find.byKey(const Key('email_field')), 'new@example.com');

        await tester.tap(find.text('Register'));
        await tester.pumpAndSettle();

        // Should show error snackbar
        expect(find.text('Registration failed. Please try again.'), findsOneWidget);
      });
    });

    group('Navigation', () {
      testWidgets('should navigate to blogs screen on successful login', (WidgetTester tester) async {
        when(mockAuthService.login(any, any)).thenAnswer((_) async => true);

        await tester.pumpWidget(
          MaterialApp(
            initialRoute: '/login',
            routes: {
              '/login': (context) => ChangeNotifierProvider<AuthService>.value(
                value: mockAuthService,
                child: const LoginScreen(),
              ),
              '/blogs': (context) => const Scaffold(body: Text('Blogs Screen')),
            },
          ),
        );

        // Fill and submit form
        await tester.enterText(find.byKey(const Key('username_field')), 'testuser');
        await tester.enterText(find.byKey(const Key('password_field')), 'password123');
        await tester.tap(find.text('Login'));
        await tester.pumpAndSettle();

        // Should navigate to blogs screen
        expect(find.text('Blogs Screen'), findsOneWidget);
      });
    });

    group('Accessibility', () {
      testWidgets('should have proper semantics for screen readers', (WidgetTester tester) async {
        await tester.pumpWidget(createLoginScreen());

        // Check for semantic labels
        expect(find.bySemanticsLabel('Username'), findsOneWidget);
        expect(find.bySemanticsLabel('Password'), findsOneWidget);
        expect(find.bySemanticsLabel('Login'), findsOneWidget);
      });

      testWidgets('should support keyboard navigation', (WidgetTester tester) async {
        await tester.pumpWidget(createLoginScreen());

        // Test tab navigation
        await tester.sendKeyEvent(LogicalKeyboardKey.tab);
        await tester.sendKeyEvent(LogicalKeyboardKey.tab);
        await tester.sendKeyEvent(LogicalKeyboardKey.enter);

        await tester.pumpAndSettle();
      });
    });
  });
}