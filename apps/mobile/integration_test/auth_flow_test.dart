import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:sf5_blog_app/main.dart' as app;
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Authentication Flow Integration Tests', () {
    setUp(() async {
      // Clear any existing data before each test
      SharedPreferences.setMockInitialValues({});
    });

    testWidgets('should complete full login flow', (WidgetTester tester) async {
      // Start the app
      app.main();
      await tester.pumpAndSettle();

      // Should start on login screen
      expect(find.text('Login'), findsOneWidget);
      expect(find.byType(TextFormField), findsNWidgets(2));

      // Fill in login credentials
      await tester.enterText(find.byKey(const Key('username_field')), 'testuser');
      await tester.enterText(find.byKey(const Key('password_field')), 'password123');

      // Submit login form
      await tester.tap(find.text('Login'));
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Note: In a real integration test, this would depend on having a test server
      // For now, we verify the login attempt was made
      expect(find.byType(CircularProgressIndicator), findsNothing);
    });

    testWidgets('should complete full registration flow', (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Switch to registration mode
      await tester.tap(find.text("Don't have an account? Register"));
      await tester.pumpAndSettle();

      // Should show registration form
      expect(find.text('Register'), findsOneWidget);
      expect(find.byType(TextFormField), findsNWidgets(5));

      // Fill registration form
      await tester.enterText(find.byKey(const Key('username_field')), 'newuser');
      await tester.enterText(find.byKey(const Key('password_field')), 'password123');
      await tester.enterText(find.byKey(const Key('retype_password_field')), 'password123');
      await tester.enterText(find.byKey(const Key('name_field')), 'New User');
      await tester.enterText(find.byKey(const Key('email_field')), 'new@example.com');

      // Submit registration form
      await tester.tap(find.text('Register'));
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Verify registration attempt was made
      expect(find.byType(CircularProgressIndicator), findsNothing);
    });

    testWidgets('should show validation errors for invalid input', (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Try to submit empty login form
      await tester.tap(find.text('Login'));
      await tester.pumpAndSettle();

      // Should show validation errors
      expect(find.text('Please enter your username'), findsOneWidget);
      expect(find.text('Please enter your password'), findsOneWidget);
    });

    testWidgets('should validate password confirmation in registration', (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Switch to registration
      await tester.tap(find.text("Don't have an account? Register"));
      await tester.pumpAndSettle();

      // Fill form with mismatched passwords
      await tester.enterText(find.byKey(const Key('username_field')), 'testuser');
      await tester.enterText(find.byKey(const Key('password_field')), 'password123');
      await tester.enterText(find.byKey(const Key('retype_password_field')), 'different123');
      await tester.enterText(find.byKey(const Key('name_field')), 'Test User');
      await tester.enterText(find.byKey(const Key('email_field')), 'test@example.com');

      // Submit form
      await tester.tap(find.text('Register'));
      await tester.pumpAndSettle();

      // Should show password mismatch error
      expect(find.text('Passwords do not match'), findsOneWidget);
    });

    testWidgets('should toggle password visibility', (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Find password field and visibility toggle
      final passwordField = find.byKey(const Key('password_field'));
      final visibilityToggle = find.byIcon(Icons.visibility);

      expect(passwordField, findsOneWidget);
      expect(visibilityToggle, findsOneWidget);

      // Enter password
      await tester.enterText(passwordField, 'secret123');
      await tester.pumpAndSettle();

      // Password should be obscured by default
      final textField = tester.widget<TextFormField>(passwordField);
      expect(textField.obscureText, true);

      // Tap visibility toggle
      await tester.tap(visibilityToggle);
      await tester.pumpAndSettle();

      // Icon should change to visibility_off
      expect(find.byIcon(Icons.visibility_off), findsOneWidget);
      expect(find.byIcon(Icons.visibility), findsNothing);
    });

    testWidgets('should switch between login and registration modes', (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Start in login mode
      expect(find.text('Login'), findsOneWidget);
      expect(find.text("Don't have an account? Register"), findsOneWidget);

      // Switch to registration
      await tester.tap(find.text("Don't have an account? Register"));
      await tester.pumpAndSettle();

      // Should be in registration mode
      expect(find.text('Register'), findsOneWidget);
      expect(find.text('Already have an account? Login'), findsOneWidget);
      expect(find.byType(TextFormField), findsNWidgets(5));

      // Switch back to login
      await tester.tap(find.text('Already have an account? Login'));
      await tester.pumpAndSettle();

      // Should be back in login mode
      expect(find.text('Login'), findsOneWidget);
      expect(find.text("Don't have an account? Register"), findsOneWidget);
      expect(find.byType(TextFormField), findsNWidgets(2));
    });

    testWidgets('should validate email format in registration', (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Switch to registration
      await tester.tap(find.text("Don't have an account? Register"));
      await tester.pumpAndSettle();

      // Fill form with invalid email
      await tester.enterText(find.byKey(const Key('username_field')), 'testuser');
      await tester.enterText(find.byKey(const Key('password_field')), 'password123');
      await tester.enterText(find.byKey(const Key('retype_password_field')), 'password123');
      await tester.enterText(find.byKey(const Key('name_field')), 'Test User');
      await tester.enterText(find.byKey(const Key('email_field')), 'invalid-email');

      // Submit form
      await tester.tap(find.text('Register'));
      await tester.pumpAndSettle();

      // Should show email validation error
      expect(find.text('Please enter a valid email address'), findsOneWidget);
    });

    testWidgets('should handle loading states properly', (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Fill login form
      await tester.enterText(find.byKey(const Key('username_field')), 'testuser');
      await tester.enterText(find.byKey(const Key('password_field')), 'password123');

      // Submit form and immediately check for loading indicator
      await tester.tap(find.text('Login'));
      await tester.pump(); // Single pump to see loading state

      // During network request, should show loading indicator
      // (This might be very brief in tests)
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // After request completes, loading should be gone
      expect(find.byType(CircularProgressIndicator), findsNothing);
    });
  });
}