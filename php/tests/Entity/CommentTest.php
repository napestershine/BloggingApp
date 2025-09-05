<?php

namespace App\Tests\Entity;

use App\Entity\Comment;
use App\Entity\BlogPost;
use App\Entity\User;
use PHPUnit\Framework\TestCase;

class CommentTest extends TestCase
{
    private Comment $comment;
    private User $user;
    private BlogPost $blogPost;

    protected function setUp(): void
    {
        $this->comment = new Comment();
        $this->user = new User();
        $this->user->setUsername('testuser');
        $this->blogPost = new BlogPost();
    }

    public function testGettersAndSetters(): void
    {
        $content = 'This is a test comment content.';
        $published = new \DateTime('2023-01-01 12:00:00');

        $this->comment->setContent($content);
        $this->comment->setPublished($published);
        $this->comment->setAuthor($this->user);
        $this->comment->setBlogPost($this->blogPost);

        $this->assertEquals($content, $this->comment->getContent());
        $this->assertEquals($published, $this->comment->getPublished());
        $this->assertSame($this->user, $this->comment->getAuthor());
        $this->assertSame($this->blogPost, $this->comment->getBlogPost());
    }

    public function testIdIsNullByDefault(): void
    {
        $this->assertNull($this->comment->getId());
    }

    public function testFluentInterface(): void
    {
        $published = new \DateTime();
        
        $result = $this->comment->setContent('Test content')
            ->setBlogPost($this->blogPost);

        $this->assertSame($this->comment, $result);
        
        // Test published date interface
        $publishedResult = $this->comment->setPublished($published);
        $this->assertSame($this->comment, $publishedResult);

        // Test authored entity interface
        $authorResult = $this->comment->setAuthor($this->user);
        $this->assertSame($this->comment, $authorResult);
    }

    public function testImplementsInterfaces(): void
    {
        $this->assertInstanceOf(\App\Entity\AuthoredEntityInterface::class, $this->comment);
        $this->assertInstanceOf(\App\Entity\PublishedDateEntityInterface::class, $this->comment);
    }

    public function testAuthorRelationship(): void
    {
        $this->comment->setAuthor($this->user);
        
        $this->assertSame($this->user, $this->comment->getAuthor());
    }

    public function testBlogPostRelationship(): void
    {
        $this->comment->setBlogPost($this->blogPost);
        
        $this->assertSame($this->blogPost, $this->comment->getBlogPost());
    }

    public function testPublishedDateHandling(): void
    {
        $date = new \DateTime('2023-06-15 14:30:00');
        
        $this->comment->setPublished($date);
        
        $this->assertEquals($date, $this->comment->getPublished());
        $this->assertInstanceOf(\DateTimeInterface::class, $this->comment->getPublished());
    }
}