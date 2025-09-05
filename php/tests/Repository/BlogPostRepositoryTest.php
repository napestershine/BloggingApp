<?php

namespace App\Tests\Repository;

use App\Entity\BlogPost;
use App\Entity\User;
use App\Repository\BlogPostRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

class BlogPostRepositoryTest extends KernelTestCase
{
    private EntityManagerInterface $entityManager;
    private BlogPostRepository $blogPostRepository;

    protected function setUp(): void
    {
        $kernel = self::bootKernel();
        $this->entityManager = $kernel->getContainer()
            ->get('doctrine')
            ->getManager();
            
        $this->blogPostRepository = $this->entityManager->getRepository(BlogPost::class);
    }

    protected function tearDown(): void
    {
        parent::tearDown();
        $this->entityManager->close();
        $this->entityManager = null;
    }

    public function testRepositoryIsInstanceOfServiceEntityRepository(): void
    {
        $this->assertInstanceOf(BlogPostRepository::class, $this->blogPostRepository);
    }

    public function testFindAllReturnsArray(): void
    {
        $blogPosts = $this->blogPostRepository->findAll();
        $this->assertIsArray($blogPosts);
    }

    public function testFindBySlugReturnsCorrectPost(): void
    {
        // Create a test user first
        $user = new User();
        $user->setUsername('blogauthor');
        $user->setPassword('TestPassword123');
        $user->setName('Blog Author');
        $user->setEmail('author@blog.com');
        $user->setRetypedPassword('TestPassword123');

        $this->entityManager->persist($user);

        // Create a test blog post
        $blogPost = new BlogPost();
        $blogPost->setTitle('Test Blog Post Title');
        $blogPost->setContent('This is a test blog post content that is longer than 20 characters.');
        $blogPost->setSlug('test-blog-post-slug');
        $blogPost->setPublished(new \DateTime());
        $blogPost->setAuthor($user);

        $this->entityManager->persist($blogPost);
        $this->entityManager->flush();

        // Test finding by slug
        $foundPost = $this->blogPostRepository->findOneBy(['slug' => 'test-blog-post-slug']);
        
        $this->assertNotNull($foundPost);
        $this->assertEquals('Test Blog Post Title', $foundPost->getTitle());
        $this->assertEquals('test-blog-post-slug', $foundPost->getSlug());
        $this->assertSame($user, $foundPost->getAuthor());

        // Cleanup
        $this->entityManager->remove($blogPost);
        $this->entityManager->remove($user);
        $this->entityManager->flush();
    }

    public function testFindByAuthorReturnsCorrectPosts(): void
    {
        // Create a test user
        $user = new User();
        $user->setUsername('specificauthor');
        $user->setPassword('TestPassword123');
        $user->setName('Specific Author');
        $user->setEmail('specific@author.com');
        $user->setRetypedPassword('TestPassword123');

        $this->entityManager->persist($user);

        // Create multiple blog posts for this author
        $blogPost1 = new BlogPost();
        $blogPost1->setTitle('First Post');
        $blogPost1->setContent('Content of the first post that is long enough.');
        $blogPost1->setSlug('first-post');
        $blogPost1->setPublished(new \DateTime());
        $blogPost1->setAuthor($user);

        $blogPost2 = new BlogPost();
        $blogPost2->setTitle('Second Post');
        $blogPost2->setContent('Content of the second post that is long enough.');
        $blogPost2->setSlug('second-post');
        $blogPost2->setPublished(new \DateTime());
        $blogPost2->setAuthor($user);

        $this->entityManager->persist($blogPost1);
        $this->entityManager->persist($blogPost2);
        $this->entityManager->flush();

        // Test finding by author
        $foundPosts = $this->blogPostRepository->findBy(['author' => $user]);
        
        $this->assertCount(2, $foundPosts);
        
        // Cleanup
        $this->entityManager->remove($blogPost1);
        $this->entityManager->remove($blogPost2);
        $this->entityManager->remove($user);
        $this->entityManager->flush();
    }

    public function testRepositoryCountWorksCorrectly(): void
    {
        $initialCount = count($this->blogPostRepository->findAll());
        
        // Create test data
        $user = new User();
        $user->setUsername('countauthor');
        $user->setPassword('TestPassword123');
        $user->setName('Count Author');
        $user->setEmail('count@author.com');
        $user->setRetypedPassword('TestPassword123');

        $this->entityManager->persist($user);

        $blogPost = new BlogPost();
        $blogPost->setTitle('Count Test Post');
        $blogPost->setContent('This is content for counting test that is long enough.');
        $blogPost->setSlug('count-test-post');
        $blogPost->setPublished(new \DateTime());
        $blogPost->setAuthor($user);

        $this->entityManager->persist($blogPost);
        $this->entityManager->flush();

        $newCount = count($this->blogPostRepository->findAll());
        $this->assertEquals($initialCount + 1, $newCount);

        // Cleanup
        $this->entityManager->remove($blogPost);
        $this->entityManager->remove($user);
        $this->entityManager->flush();
    }
}