<?php

namespace App\Tests\EventSubscriber;

use App\Entity\PublishedDateEntityInterface;
use App\EventSubscriber\PublishedDateEntitySubscriber;
use PHPUnit\Framework\TestCase;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpKernel\Event\ViewEvent;
use Symfony\Component\HttpKernel\KernelEvents;
use Symfony\Component\HttpKernel\HttpKernelInterface;
use ApiPlatform\Symfony\EventListener\EventPriorities;

class PublishedDateEntitySubscriberTest extends TestCase
{
    private PublishedDateEntitySubscriber $subscriber;

    protected function setUp(): void
    {
        $this->subscriber = new PublishedDateEntitySubscriber();
    }

    public function testGetSubscribedEvents(): void
    {
        $events = PublishedDateEntitySubscriber::getSubscribedEvents();
        
        $this->assertArrayHasKey(KernelEvents::VIEW, $events);
        $this->assertEquals(['setDatePublished', EventPriorities::PRE_WRITE], $events[KernelEvents::VIEW]);
    }

    public function testSetsPublishedDateOnPostRequest(): void
    {
        $entity = $this->createMock(PublishedDateEntityInterface::class);
        
        $request = new Request();
        $request->setMethod(Request::METHOD_POST);
        
        $kernel = $this->createMock(HttpKernelInterface::class);
        $event = new ViewEvent($kernel, $request, HttpKernelInterface::MAIN_REQUEST, $entity);
        
        $entity->expects($this->once())
            ->method('setPublished')
            ->with($this->isInstanceOf(\DateTime::class));
        
        $this->subscriber->setDatePublished($event);
    }

    public function testDoesNotSetPublishedDateOnGetRequest(): void
    {
        $entity = $this->createMock(PublishedDateEntityInterface::class);
        
        $request = new Request();
        $request->setMethod(Request::METHOD_GET);
        
        $kernel = $this->createMock(HttpKernelInterface::class);
        $event = new ViewEvent($kernel, $request, HttpKernelInterface::MAIN_REQUEST, $entity);
        
        $entity->expects($this->never())
            ->method('setPublished');
        
        $this->subscriber->setDatePublished($event);
    }

    public function testDoesNotSetPublishedDateOnNonPublishedDateEntity(): void
    {
        $entity = new \stdClass();
        
        $request = new Request();
        $request->setMethod(Request::METHOD_POST);
        
        $kernel = $this->createMock(HttpKernelInterface::class);
        $event = new ViewEvent($kernel, $request, HttpKernelInterface::MAIN_REQUEST, $entity);
        
        // Should not throw an exception and should not call setPublished
        $this->subscriber->setDatePublished($event);
        
        // If we get here without exception, the test passes
        $this->assertTrue(true);
    }

    public function testPublishedDateIsCurrentDateTime(): void
    {
        $entity = $this->createMock(PublishedDateEntityInterface::class);
        
        $request = new Request();
        $request->setMethod(Request::METHOD_POST);
        
        $kernel = $this->createMock(HttpKernelInterface::class);
        $event = new ViewEvent($kernel, $request, HttpKernelInterface::MAIN_REQUEST, $entity);
        
        $beforeTime = new \DateTime();
        
        $entity->expects($this->once())
            ->method('setPublished')
            ->with($this->callback(function (\DateTime $dateTime) use ($beforeTime) {
                $afterTime = new \DateTime();
                return $dateTime >= $beforeTime && $dateTime <= $afterTime;
            }));
        
        $this->subscriber->setDatePublished($event);
    }

    public function testDoesNotSetPublishedDateOnPutRequest(): void
    {
        $entity = $this->createMock(PublishedDateEntityInterface::class);
        
        $request = new Request();
        $request->setMethod(Request::METHOD_PUT);
        
        $kernel = $this->createMock(HttpKernelInterface::class);
        $event = new ViewEvent($kernel, $request, HttpKernelInterface::MAIN_REQUEST, $entity);
        
        $entity->expects($this->never())
            ->method('setPublished');
        
        $this->subscriber->setDatePublished($event);
    }
}