<?php

declare(strict_types=1);

namespace App\EventSubscriber;

use ApiPlatform\Symfony\EventListener\EventPriorities;
use App\Entity\PublishedDateEntityInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpKernel\Event\ViewEvent;
use Symfony\Component\HttpKernel\KernelEvents;

/**
 * Class PublishedDateEntitySubscriber
 * @package App\EventSubscriber
 */
class PublishedDateEntitySubscriber implements EventSubscriberInterface
{
    /**
     * @return array
     */
    public static function getSubscribedEvents()
    {
        return [
            KernelEvents::VIEW => ['setDatePublished', EventPriorities::PRE_WRITE],
        ];
    }

    /**
     * @param ViewEvent $event
     * @throws \Exception
     */
    public function setDatePublished(ViewEvent $event)
    {
        $entity = $event->getControllerResult();
        $method = $event->getRequest()->getMethod();

        if (!($entity instanceof PublishedDateEntityInterface) || Request::METHOD_POST !== $method) {
            return;
        }

        $entity->setPublished(new \DateTime());
    }
}
