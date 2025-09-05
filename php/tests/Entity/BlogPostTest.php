<?php

namespace App\Tests\Entity;

use App\Entity\BlogPost;
use App\Entity\User;
use PHPUnit\Framework\TestCase;

class BlogPostTest extends TestCase
{
    private BlogPost $blogPost;
    private User $user;

    protected function setUp(): void
    {
        $this->blogPost = new BlogPost();
        $this->user = new User();
        $this->user->setUsername('testuser');
    }

    public function testGettersAndSetters(): void
    {
        $title = 'Test Blog Post Title';
        $content = 'This is a test blog post content that is longer than 20 characters.';
        $slug = 'test-blog-post-title';
        $published = new \DateTime('2023-01-01 12:00:00');

        $this->blogPost->setTitle($title);
        $this->blogPost->setContent($content);
        $this->blogPost->setSlug($slug);
        $this->blogPost->setPublished($published);
        $this->blogPost->setAuthor($this->user);

        $this->assertEquals($title, $this->blogPost->getTitle());
        $this->assertEquals($content, $this->blogPost->getContent());
        $this->assertEquals($slug, $this->blogPost->getSlug());
        $this->assertEquals($published, $this->blogPost->getPublished());
        $this->assertSame($this->user, $this->blogPost->getAuthor());
    }

    public function testCommentsCollectionInitialization(): void
    {
        $this->assertCount(0, $this->blogPost->getComments());
    }

    public function testIdIsNullByDefault(): void
    {
        $this->assertNull($this->blogPost->getId());
    }

    public function testFluentInterface(): void
    {
        $published = new \DateTime();
        
        $result = $this->blogPost->setTitle('Test Title')
            ->setContent('Test content')
            ->setSlug('test-slug')
            ->setAuthor($this->user);

        $this->assertSame($this->blogPost, $result);
        
        // Test published date interface
        $publishedResult = $this->blogPost->setPublished($published);
        $this->assertSame($this->blogPost, $publishedResult);
    }

    public function testImplementsInterfaces(): void
    {
        $this->assertInstanceOf(\App\Entity\AuthoredEntityInterface::class, $this->blogPost);
        $this->assertInstanceOf(\App\Entity\PublishedDateEntityInterface::class, $this->blogPost);
    }

    public function testAuthorRelationship(): void
    {
        $this->blogPost->setAuthor($this->user);
        
        $this->assertSame($this->user, $this->blogPost->getAuthor());
    }

    public function testPublishedDateHandling(): void
    {
        $date = new \DateTime('2023-06-15 14:30:00');
        
        $this->blogPost->setPublished($date);
        
        $this->assertEquals($date, $this->blogPost->getPublished());
        $this->assertInstanceOf(\DateTimeInterface::class, $this->blogPost->getPublished());
    }
}