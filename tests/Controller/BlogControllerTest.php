<?php

namespace App\Tests\Controller;

use App\Entity\BlogPost;
use App\Entity\User;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;
use Symfony\Component\HttpFoundation\Response;

class BlogControllerTest extends WebTestCase
{
    private $entityManager;

    protected function setUp(): void
    {
        $kernel = self::bootKernel();
        $this->entityManager = $kernel->getContainer()
            ->get('doctrine')
            ->getManager();
    }

    protected function tearDown(): void
    {
        parent::tearDown();
        $this->entityManager->close();
        $this->entityManager = null;
    }

    public function testListEndpoint(): void
    {
        $client = static::createClient();
        
        $client->request('GET', '/blog/1');
        
        $this->assertResponseIsSuccessful();
        $this->assertResponseHeaderSame('content-type', 'application/json');
        
        $content = json_decode($client->getResponse()->getContent(), true);
        $this->assertArrayHasKey('page', $content);
        $this->assertArrayHasKey('limit', $content);
        $this->assertArrayHasKey('data', $content);
    }

    public function testListWithCustomLimit(): void
    {
        $client = static::createClient();
        
        $client->request('GET', '/blog/1?limit=5');
        
        $this->assertResponseIsSuccessful();
        
        $content = json_decode($client->getResponse()->getContent(), true);
        $this->assertEquals(5, $content['limit']);
    }

    public function testPostByIdNotFound(): void
    {
        $client = static::createClient();
        
        $client->request('GET', '/blog/post/999999');
        
        $this->assertResponseIsSuccessful();
        $response = $client->getResponse();
        $this->assertEquals('null', $response->getContent());
    }

    public function testPostBySlugNotFound(): void
    {
        $client = static::createClient();
        
        $client->request('GET', '/blog/post/non-existent-slug');
        
        $this->assertResponseIsSuccessful();
        $response = $client->getResponse();
        $this->assertEquals('null', $response->getContent());
    }

    public function testAddPostWithoutAuthentication(): void
    {
        $client = static::createClient();
        
        $postData = [
            'title' => 'Test Blog Post',
            'content' => 'This is a test blog post content that is more than 20 characters long.',
            'slug' => 'test-blog-post'
        ];
        
        $client->request(
            'POST',
            '/blog/add',
            [],
            [],
            ['CONTENT_TYPE' => 'application/json'],
            json_encode($postData)
        );
        
        // This should fail because we're not authenticated
        // The exact response depends on security configuration
        $this->assertNotEquals(Response::HTTP_CREATED, $client->getResponse()->getStatusCode());
    }

    public function testDeletePostNotFound(): void
    {
        $client = static::createClient();
        
        $client->request('DELETE', '/blog/post/999999');
        
        // This should fail because the post doesn't exist
        // and we're likely not authenticated
        $this->assertNotEquals(Response::HTTP_NO_CONTENT, $client->getResponse()->getStatusCode());
    }

    public function testListDefaultPage(): void
    {
        $client = static::createClient();
        
        $client->request('GET', '/blog/');
        
        $this->assertResponseIsSuccessful();
        
        $content = json_decode($client->getResponse()->getContent(), true);
        $this->assertEquals(5, $content['page']); // Default page from route
    }

    public function testResponseFormat(): void
    {
        $client = static::createClient();
        
        $client->request('GET', '/blog/1');
        
        $this->assertResponseIsSuccessful();
        $this->assertJson($client->getResponse()->getContent());
        
        $content = json_decode($client->getResponse()->getContent(), true);
        $this->assertIsArray($content);
        $this->assertArrayHasKey('page', $content);
        $this->assertArrayHasKey('limit', $content);
        $this->assertArrayHasKey('data', $content);
        $this->assertIsArray($content['data']);
    }
}