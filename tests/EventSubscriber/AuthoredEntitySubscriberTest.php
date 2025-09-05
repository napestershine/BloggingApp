<?php

namespace App\Tests\EventSubscriber;

use App\Entity\AuthoredEntityInterface;
use App\EventSubscriber\AuthoredEntitySubscriber;
use PHPUnit\Framework\TestCase;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpKernel\Event\ViewEvent;
use Symfony\Component\HttpKernel\KernelEvents;
use Symfony\Component\HttpKernel\HttpKernelInterface;
use Symfony\Component\Security\Core\Authentication\Token\Storage\TokenStorageInterface;
use Symfony\Component\Security\Core\Authentication\Token\TokenInterface;
use Symfony\Component\Security\Core\User\UserInterface;
use ApiPlatform\Symfony\EventListener\EventPriorities;

class AuthoredEntitySubscriberTest extends TestCase
{
    private AuthoredEntitySubscriber $subscriber;
    private TokenStorageInterface $tokenStorage;
    private TokenInterface $token;
    private UserInterface $user;

    protected function setUp(): void
    {
        $this->tokenStorage = $this->createMock(TokenStorageInterface::class);
        $this->token = $this->createMock(TokenInterface::class);
        $this->user = $this->createMock(UserInterface::class);
        
        $this->subscriber = new AuthoredEntitySubscriber($this->tokenStorage);
    }

    public function testGetSubscribedEvents(): void
    {
        $events = AuthoredEntitySubscriber::getSubscribedEvents();
        
        $this->assertArrayHasKey(KernelEvents::VIEW, $events);
        $this->assertEquals(['getAuthenticatedUser', EventPriorities::PRE_WRITE], $events[KernelEvents::VIEW]);
    }

    public function testSetsAuthorOnPostRequest(): void
    {
        $entity = $this->createMock(AuthoredEntityInterface::class);
        
        $request = new Request();
        $request->setMethod(Request::METHOD_POST);
        
        $kernel = $this->createMock(HttpKernelInterface::class);
        $event = new ViewEvent($kernel, $request, HttpKernelInterface::MAIN_REQUEST, $entity);
        
        $this->tokenStorage->expects($this->once())
            ->method('getToken')
            ->willReturn($this->token);
            
        $this->token->expects($this->once())
            ->method('getUser')
            ->willReturn($this->user);
            
        $entity->expects($this->once())
            ->method('setAuthor')
            ->with($this->user);
        
        $this->subscriber->getAuthenticatedUser($event);
    }

    public function testDoesNotSetAuthorOnGetRequest(): void
    {
        $entity = $this->createMock(AuthoredEntityInterface::class);
        
        $request = new Request();
        $request->setMethod(Request::METHOD_GET);
        
        $kernel = $this->createMock(HttpKernelInterface::class);
        $event = new ViewEvent($kernel, $request, HttpKernelInterface::MAIN_REQUEST, $entity);
        
        $this->tokenStorage->expects($this->never())
            ->method('getToken');
            
        $entity->expects($this->never())
            ->method('setAuthor');
        
        $this->subscriber->getAuthenticatedUser($event);
    }

    public function testDoesNotSetAuthorOnNonAuthoredEntity(): void
    {
        $entity = new \stdClass();
        
        $request = new Request();
        $request->setMethod(Request::METHOD_POST);
        
        $kernel = $this->createMock(HttpKernelInterface::class);
        $event = new ViewEvent($kernel, $request, HttpKernelInterface::MAIN_REQUEST, $entity);
        
        $this->tokenStorage->expects($this->never())
            ->method('getToken');
        
        $this->subscriber->getAuthenticatedUser($event);
    }

    public function testConstructorSetsTokenStorage(): void
    {
        $subscriber = new AuthoredEntitySubscriber($this->tokenStorage);
        
        // Use reflection to access private property
        $reflection = new \ReflectionClass($subscriber);
        $property = $reflection->getProperty('tokenStorage');
        $property->setAccessible(true);
        
        $this->assertSame($this->tokenStorage, $property->getValue($subscriber));
    }
}