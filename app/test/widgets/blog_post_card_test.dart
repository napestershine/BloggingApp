import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:sf5_blog_app/widgets/blog_post_card.dart';
import 'package:sf5_blog_app/models/blog_post.dart';
import 'package:sf5_blog_app/models/user.dart';
import 'package:sf5_blog_app/models/comment.dart';

void main() {
  group('BlogPostCard Widget Tests', () {
    
    Widget createBlogPostCard({
      required BlogPost blogPost,
      VoidCallback? onTap,
    }) {
      return MaterialApp(
        home: Scaffold(
          body: BlogPostCard(
            blogPost: blogPost,
            onTap: onTap,
          ),
        ),
      );
    }

    group('Display Content', () {
      testWidgets('should display blog post title and content', (WidgetTester tester) async {
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Blog Post',
          content: 'This is a test blog post content with some details.',
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.text('Test Blog Post'), findsOneWidget);
        expect(find.text('This is a test blog post content with some details.'), findsOneWidget);
      });

      testWidgets('should truncate long title with ellipsis', (WidgetTester tester) async {
        final blogPost = BlogPost(
          id: 1,
          title: 'This is a very long blog post title that should be truncated with ellipsis when displayed in the card widget',
          content: 'Short content',
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));
        
        final titleWidget = tester.widget<Text>(find.text(blogPost.title));
        expect(titleWidget.maxLines, 2);
        expect(titleWidget.overflow, TextOverflow.ellipsis);
      });

      testWidgets('should truncate long content with ellipsis', (WidgetTester tester) async {
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Title',
          content: 'This is a very long blog post content that should be truncated with ellipsis when displayed in the card widget. It contains multiple sentences and should only show the first few lines.',
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));
        
        final contentText = find.text(blogPost.content);
        expect(contentText, findsOneWidget);
        
        final contentWidget = tester.widget<Text>(contentText);
        expect(contentWidget.maxLines, 3);
        expect(contentWidget.overflow, TextOverflow.ellipsis);
      });
    });

    group('Author Information', () {
      testWidgets('should display author name when available', (WidgetTester tester) async {
        final author = User(
          id: 1,
          username: 'testuser',
          name: 'Test Author',
        );
        
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
          author: author,
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.text('By Test Author'), findsOneWidget);
        expect(find.byIcon(Icons.person), findsOneWidget);
      });

      testWidgets('should not display author section when author is null', (WidgetTester tester) async {
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
          author: null,
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.text('By'), findsNothing);
        expect(find.byIcon(Icons.person), findsNothing);
      });
    });

    group('Published Date', () {
      testWidgets('should display formatted date when available', (WidgetTester tester) async {
        final publishedDate = DateTime(2024, 1, 15, 10, 30);
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
          publishedDate: publishedDate,
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.byIcon(Icons.schedule), findsOneWidget);
        // The exact text depends on the current date, so we just check for a date-like pattern
        expect(find.textContaining('15/1/2024'), findsOneWidget);
      });

      testWidgets('should format recent dates as relative time', (WidgetTester tester) async {
        // Date 2 hours ago
        final publishedDate = DateTime.now().subtract(const Duration(hours: 2));
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
          publishedDate: publishedDate,
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.textContaining('2 hours ago'), findsOneWidget);
        expect(find.byIcon(Icons.schedule), findsOneWidget);
      });

      testWidgets('should not display date section when publishedDate is null', (WidgetTester tester) async {
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
          publishedDate: null,
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.byIcon(Icons.schedule), findsNothing);
      });
    });

    group('Comments', () {
      testWidgets('should display comment count when comments exist', (WidgetTester tester) async {
        final comments = [
          Comment(id: 1, content: 'Comment 1'),
          Comment(id: 2, content: 'Comment 2'),
          Comment(id: 3, content: 'Comment 3'),
        ];
        
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
          comments: comments,
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.text('3 comments'), findsOneWidget);
        expect(find.byIcon(Icons.comment_outlined), findsOneWidget);
      });

      testWidgets('should display "No comments" when no comments exist', (WidgetTester tester) async {
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
          comments: [],
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.text('No comments'), findsOneWidget);
        expect(find.byIcon(Icons.comment_outlined), findsOneWidget);
      });

      testWidgets('should display "No comments" when comments is null', (WidgetTester tester) async {
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
          comments: null,
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.text('No comments'), findsOneWidget);
        expect(find.byIcon(Icons.comment_outlined), findsOneWidget);
      });
    });

    group('Interactions', () {
      testWidgets('should call onTap when card is tapped', (WidgetTester tester) async {
        bool tapped = false;
        void onTap() {
          tapped = true;
        }

        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
        );

        await tester.pumpWidget(createBlogPostCard(
          blogPost: blogPost,
          onTap: onTap,
        ));

        await tester.tap(find.byType(InkWell));
        await tester.pumpAndSettle();

        expect(tapped, true);
      });

      testWidgets('should not crash when onTap is null and card is tapped', (WidgetTester tester) async {
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        await tester.tap(find.byType(InkWell));
        await tester.pumpAndSettle();

        // Should not throw any exceptions
      });

      testWidgets('should have proper tap feedback with InkWell', (WidgetTester tester) async {
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.byType(InkWell), findsOneWidget);
        
        final inkWell = tester.widget<InkWell>(find.byType(InkWell));
        expect(inkWell.borderRadius, BorderRadius.circular(12));
      });
    });

    group('Visual Elements', () {
      testWidgets('should display arrow forward icon', (WidgetTester tester) async {
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.byIcon(Icons.arrow_forward_ios), findsOneWidget);
      });

      testWidgets('should be wrapped in a Card widget', (WidgetTester tester) async {
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.byType(Card), findsOneWidget);
        
        final card = tester.widget<Card>(find.byType(Card));
        expect(card.margin, const EdgeInsets.only(bottom: 16));
      });

      testWidgets('should have proper padding', (WidgetTester tester) async {
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        final padding = find.widgetWithText(Padding, 'Test Post');
        expect(padding, findsOneWidget);
        
        final paddingWidget = tester.widget<Padding>(padding);
        expect(paddingWidget.padding, const EdgeInsets.all(16));
      });
    });

    group('Date Formatting', () {
      testWidgets('should format "just now" for very recent posts', (WidgetTester tester) async {
        final publishedDate = DateTime.now().subtract(const Duration(seconds: 30));
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
          publishedDate: publishedDate,
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.text('Just now'), findsOneWidget);
      });

      testWidgets('should format minutes ago correctly', (WidgetTester tester) async {
        final publishedDate = DateTime.now().subtract(const Duration(minutes: 30));
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
          publishedDate: publishedDate,
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.text('30 minutes ago'), findsOneWidget);
      });

      testWidgets('should format single day ago correctly', (WidgetTester tester) async {
        final publishedDate = DateTime.now().subtract(const Duration(days: 1));
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
          publishedDate: publishedDate,
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.text('1 day ago'), findsOneWidget);
      });

      testWidgets('should format multiple days ago correctly', (WidgetTester tester) async {
        final publishedDate = DateTime.now().subtract(const Duration(days: 5));
        final blogPost = BlogPost(
          id: 1,
          title: 'Test Post',
          content: 'Test content',
          publishedDate: publishedDate,
        );

        await tester.pumpWidget(createBlogPostCard(blogPost: blogPost));

        expect(find.text('5 days ago'), findsOneWidget);
      });
    });
  });
}