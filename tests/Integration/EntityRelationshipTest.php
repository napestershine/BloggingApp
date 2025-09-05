<?php

namespace App\Tests\Integration;

use App\Entity\BlogPost;
use App\Entity\Comment;
use App\Entity\User;
use PHPUnit\Framework\TestCase;

/**
 * Integration test to verify entity relationships work correctly
 */
class EntityRelationshipTest extends TestCase
{
    public function testUserBlogPostRelationship(): void
    {
        $user = new User();
        $user->setUsername('testuser');
        $user->setPassword('TestPassword123');
        $user->setName('Test User');
        $user->setEmail('test@example.com');
        $user->setRetypedPassword('TestPassword123');

        $blogPost = new BlogPost();
        $blogPost->setTitle('Test Blog Post');
        $blogPost->setContent('This is test content that is long enough for validation.');
        $blogPost->setSlug('test-blog-post');
        $blogPost->setPublished(new \DateTime());
        $blogPost->setAuthor($user);

        // Test that the relationship is established
        $this->assertSame($user, $blogPost->getAuthor());
        
        // Test that collections are properly initialized
        $this->assertCount(0, $user->getPosts());
        $this->assertCount(0, $blogPost->getComments());
    }

    public function testBlogPostCommentRelationship(): void
    {
        $user = new User();
        $user->setUsername('commentuser');
        $user->setPassword('TestPassword123');
        $user->setName('Comment User');
        $user->setEmail('comment@example.com');
        $user->setRetypedPassword('TestPassword123');

        $blogPost = new BlogPost();
        $blogPost->setTitle('Blog Post with Comments');
        $blogPost->setContent('This blog post will have comments attached to it.');
        $blogPost->setSlug('blog-post-with-comments');
        $blogPost->setPublished(new \DateTime());
        $blogPost->setAuthor($user);

        $comment = new Comment();
        $comment->setContent('This is a test comment on the blog post.');
        $comment->setPublished(new \DateTime());
        $comment->setAuthor($user);
        $comment->setBlogPost($blogPost);

        // Test relationships
        $this->assertSame($blogPost, $comment->getBlogPost());
        $this->assertSame($user, $comment->getAuthor());
    }

    public function testUserCommentsRelationship(): void
    {
        $user = new User();
        $user->setUsername('multicommentuser');
        $user->setPassword('TestPassword123');
        $user->setName('Multi Comment User');
        $user->setEmail('multicomment@example.com');
        $user->setRetypedPassword('TestPassword123');

        $blogPost = new BlogPost();
        $blogPost->setTitle('Post for Multiple Comments');
        $blogPost->setContent('This post will receive multiple comments from the same user.');
        $blogPost->setSlug('post-for-multiple-comments');
        $blogPost->setPublished(new \DateTime());
        $blogPost->setAuthor($user);

        $comment1 = new Comment();
        $comment1->setContent('This is the first comment from this user.');
        $comment1->setPublished(new \DateTime());
        $comment1->setAuthor($user);
        $comment1->setBlogPost($blogPost);

        $comment2 = new Comment();
        $comment2->setContent('This is the second comment from the same user.');
        $comment2->setPublished(new \DateTime());
        $comment2->setAuthor($user);
        $comment2->setBlogPost($blogPost);

        // Test that both comments reference the same user and blog post
        $this->assertSame($user, $comment1->getAuthor());
        $this->assertSame($user, $comment2->getAuthor());
        $this->assertSame($blogPost, $comment1->getBlogPost());
        $this->assertSame($blogPost, $comment2->getBlogPost());

        // Test collections initialization
        $this->assertCount(0, $user->getComments());
        $this->assertCount(0, $user->getPosts());
        $this->assertCount(0, $blogPost->getComments());
    }

    public function testInterfaceImplementations(): void
    {
        $user = new User();
        $blogPost = new BlogPost();
        $comment = new Comment();

        // Test that entities implement required interfaces
        $this->assertInstanceOf(\Symfony\Component\Security\Core\User\UserInterface::class, $user);
        $this->assertInstanceOf(\App\Entity\AuthoredEntityInterface::class, $blogPost);
        $this->assertInstanceOf(\App\Entity\PublishedDateEntityInterface::class, $blogPost);
        $this->assertInstanceOf(\App\Entity\AuthoredEntityInterface::class, $comment);
        $this->assertInstanceOf(\App\Entity\PublishedDateEntityInterface::class, $comment);
    }

    public function testEntityValidationRequirements(): void
    {
        // Test User validation requirements
        $user = new User();
        $user->setUsername('validuser'); // >= 6 chars
        $user->setPassword('ValidPass123'); // Meets regex requirements
        $user->setName('Valid User'); // >= 1 char
        $user->setEmail('valid@user.com'); // Valid email
        $user->setRetypedPassword('ValidPass123'); // Matches password

        $this->assertEquals('validuser', $user->getUsername());
        $this->assertEquals('ValidPass123', $user->getPassword());
        $this->assertEquals('ValidPass123', $user->getRetypedPassword());

        // Test BlogPost validation requirements
        $blogPost = new BlogPost();
        $blogPost->setTitle('Valid Title'); // >= 10 chars
        $blogPost->setContent('This is valid content that is longer than 20 characters as required.'); // >= 20 chars
        $blogPost->setSlug('valid-slug');

        $this->assertEquals('Valid Title', $blogPost->getTitle());
        $this->assertTrue(strlen($blogPost->getContent()) >= 20);

        // Test Comment validation requirements
        $comment = new Comment();
        $comment->setContent('Valid comment content'); // >= 5 chars, <= 3000 chars

        $this->assertEquals('Valid comment content', $comment->getContent());
        $this->assertTrue(strlen($comment->getContent()) >= 5);
        $this->assertTrue(strlen($comment->getContent()) <= 3000);
    }
}