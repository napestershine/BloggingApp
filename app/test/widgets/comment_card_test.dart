import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:sf5_blog_app/widgets/comment_card.dart';
import 'package:sf5_blog_app/models/comment.dart';
import 'package:sf5_blog_app/models/user.dart';

void main() {
  group('CommentCard Widget Tests', () {
    
    Widget createCommentCard({required Comment comment}) {
      return MaterialApp(
        home: Scaffold(
          body: CommentCard(comment: comment),
        ),
      );
    }

    group('Display Content', () {
      testWidgets('should display comment content', (WidgetTester tester) async {
        final comment = Comment(
          id: 1,
          content: 'This is a test comment with some content.',
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.text('This is a test comment with some content.'), findsOneWidget);
      });

      testWidgets('should display long comment content properly', (WidgetTester tester) async {
        final comment = Comment(
          id: 1,
          content: 'This is a very long comment that contains multiple sentences and should be displayed properly without truncation. It should maintain proper text styling and readability.',
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.text(comment.content), findsOneWidget);
        
        // Verify the text widget doesn't have maxLines restriction
        final textWidget = tester.widget<Text>(find.text(comment.content));
        expect(textWidget.maxLines, null);
      });
    });

    group('Author Information', () {
      testWidgets('should display author name when available', (WidgetTester tester) async {
        final author = User(
          id: 1,
          username: 'testuser',
          name: 'Test Author',
        );
        
        final comment = Comment(
          id: 1,
          content: 'Test comment',
          author: author,
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.text('Test Author'), findsOneWidget);
        expect(find.byIcon(Icons.person), findsOneWidget);
      });

      testWidgets('should display "Anonymous" when author is null', (WidgetTester tester) async {
        final comment = Comment(
          id: 1,
          content: 'Anonymous comment',
          author: null,
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.text('Anonymous'), findsOneWidget);
        expect(find.byIcon(Icons.person), findsOneWidget);
      });

      testWidgets('should display "Anonymous" when author name is null', (WidgetTester tester) async {
        final author = User(
          id: 1,
          username: 'testuser',
          name: null,
        );
        
        final comment = Comment(
          id: 1,
          content: 'Test comment',
          author: author,
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.text('Anonymous'), findsOneWidget);
      });
    });

    group('Published Date', () {
      testWidgets('should display formatted date when available', (WidgetTester tester) async {
        final publishedDate = DateTime(2024, 1, 15, 10, 30);
        final comment = Comment(
          id: 1,
          content: 'Test comment',
          publishedDate: publishedDate,
          author: const User(username: 'testuser', name: 'Test User'),
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        // Should display date in some format
        expect(find.textContaining('15/1/2024'), findsOneWidget);
      });

      testWidgets('should format recent dates as relative time', (WidgetTester tester) async {
        // Date 3 hours ago
        final publishedDate = DateTime.now().subtract(const Duration(hours: 3));
        final comment = Comment(
          id: 1,
          content: 'Recent comment',
          publishedDate: publishedDate,
          author: const User(username: 'testuser', name: 'Test User'),
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.textContaining('3 hours ago'), findsOneWidget);
      });

      testWidgets('should not display date when publishedDate is null', (WidgetTester tester) async {
        final comment = Comment(
          id: 1,
          content: 'Test comment',
          publishedDate: null,
          author: const User(username: 'testuser', name: 'Test User'),
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        // Should only show author name, no date
        expect(find.text('Test User'), findsOneWidget);
        // No specific date text should be found
        expect(find.textContaining('ago'), findsNothing);
        expect(find.textContaining('/'), findsNothing);
      });
    });

    group('Visual Elements', () {
      testWidgets('should display avatar with person icon', (WidgetTester tester) async {
        final comment = Comment(
          id: 1,
          content: 'Test comment',
          author: const User(username: 'testuser', name: 'Test User'),
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.byType(CircleAvatar), findsOneWidget);
        expect(find.byIcon(Icons.person), findsOneWidget);
        
        // Check avatar properties
        final avatar = tester.widget<CircleAvatar>(find.byType(CircleAvatar));
        expect(avatar.radius, 16);
      });

      testWidgets('should be wrapped in a Card widget', (WidgetTester tester) async {
        final comment = Comment(
          id: 1,
          content: 'Test comment',
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.byType(Card), findsOneWidget);
        
        final card = tester.widget<Card>(find.byType(Card));
        expect(card.margin, const EdgeInsets.only(bottom: 8));
      });

      testWidgets('should have proper padding', (WidgetTester tester) async {
        final comment = Comment(
          id: 1,
          content: 'Test comment',
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        final padding = find.widgetWithText(Padding, 'Test comment');
        expect(padding, findsOneWidget);
        
        final paddingWidget = tester.widget<Padding>(padding);
        expect(paddingWidget.padding, const EdgeInsets.all(12));
      });

      testWidgets('should use proper layout structure', (WidgetTester tester) async {
        final comment = Comment(
          id: 1,
          content: 'Test comment',
          author: const User(username: 'testuser', name: 'Test User'),
          publishedDate: DateTime.now(),
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        // Should have Column as main container
        expect(find.byType(Column), findsNWidgets(2)); // Main column and author info column
        
        // Should have Row for author information
        expect(find.byType(Row), findsOneWidget);
        
        // Should have Expanded widget for flexible layout
        expect(find.byType(Expanded), findsOneWidget);
      });
    });

    group('Date Formatting', () {
      testWidgets('should format "just now" for very recent comments', (WidgetTester tester) async {
        final publishedDate = DateTime.now().subtract(const Duration(seconds: 30));
        final comment = Comment(
          id: 1,
          content: 'Very recent comment',
          publishedDate: publishedDate,
          author: const User(username: 'testuser', name: 'Test User'),
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.text('Just now'), findsOneWidget);
      });

      testWidgets('should format minutes ago correctly', (WidgetTester tester) async {
        final publishedDate = DateTime.now().subtract(const Duration(minutes: 45));
        final comment = Comment(
          id: 1,
          content: 'Comment from 45 minutes ago',
          publishedDate: publishedDate,
          author: const User(username: 'testuser', name: 'Test User'),
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.text('45 minutes ago'), findsOneWidget);
      });

      testWidgets('should format single hour ago correctly', (WidgetTester tester) async {
        final publishedDate = DateTime.now().subtract(const Duration(hours: 1));
        final comment = Comment(
          id: 1,
          content: 'Comment from 1 hour ago',
          publishedDate: publishedDate,
          author: const User(username: 'testuser', name: 'Test User'),
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.text('1 hour ago'), findsOneWidget);
      });

      testWidgets('should format multiple hours ago correctly', (WidgetTester tester) async {
        final publishedDate = DateTime.now().subtract(const Duration(hours: 5));
        final comment = Comment(
          id: 1,
          content: 'Comment from 5 hours ago',
          publishedDate: publishedDate,
          author: const User(username: 'testuser', name: 'Test User'),
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.text('5 hours ago'), findsOneWidget);
      });

      testWidgets('should format single day ago correctly', (WidgetTester tester) async {
        final publishedDate = DateTime.now().subtract(const Duration(days: 1));
        final comment = Comment(
          id: 1,
          content: 'Comment from yesterday',
          publishedDate: publishedDate,
          author: const User(username: 'testuser', name: 'Test User'),
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.text('1 day ago'), findsOneWidget);
      });

      testWidgets('should format multiple days ago correctly', (WidgetTester tester) async {
        final publishedDate = DateTime.now().subtract(const Duration(days: 4));
        final comment = Comment(
          id: 1,
          content: 'Comment from 4 days ago',
          publishedDate: publishedDate,
          author: const User(username: 'testuser', name: 'Test User'),
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.text('4 days ago'), findsOneWidget);
      });

      testWidgets('should format old dates as absolute dates', (WidgetTester tester) async {
        final publishedDate = DateTime(2023, 12, 15, 14, 30);
        final comment = Comment(
          id: 1,
          content: 'Old comment',
          publishedDate: publishedDate,
          author: const User(username: 'testuser', name: 'Test User'),
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        expect(find.text('15/12/2023'), findsOneWidget);
      });
    });

    group('Theme Integration', () {
      testWidgets('should use theme colors for avatar', (WidgetTester tester) async {
        final comment = Comment(
          id: 1,
          content: 'Test comment',
          author: const User(username: 'testuser', name: 'Test User'),
        );

        await tester.pumpWidget(
          MaterialApp(
            theme: ThemeData(
              colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
            ),
            home: Scaffold(
              body: CommentCard(comment: comment),
            ),
          ),
        );

        final avatar = tester.widget<CircleAvatar>(find.byType(CircleAvatar));
        expect(avatar.backgroundColor, isNotNull);
        
        final icon = tester.widget<Icon>(find.byIcon(Icons.person));
        expect(icon.color, isNotNull);
      });

      testWidgets('should use theme text styles', (WidgetTester tester) async {
        final comment = Comment(
          id: 1,
          content: 'Test comment content',
          author: const User(username: 'testuser', name: 'Test User'),
          publishedDate: DateTime.now(),
        );

        await tester.pumpWidget(createCommentCard(comment: comment));

        // Author name should use titleSmall style
        final authorText = find.text('Test User');
        expect(authorText, findsOneWidget);
        
        // Content should use bodyMedium style
        final contentText = find.text('Test comment content');
        expect(contentText, findsOneWidget);
      });
    });
  });
}