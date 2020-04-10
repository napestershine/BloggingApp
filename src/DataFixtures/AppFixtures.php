<?php

namespace App\DataFixtures;

use App\Entity\BlogPost;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Common\Persistence\ObjectManager;

class AppFixtures extends Fixture
{
    public function load(ObjectManager $manager)
    {
        for ($i = 1; $i < 10; $i++) {
            $blogPost = new BlogPost();
            $blogPost->setTitle('this is post title ' . $i)
                ->setPublished(new \DateTime())
                ->setContent('This is content ' . $i)
                ->setSlug('slug-title-' . $i)
                ->setAuthor('Manu')
            ;
            $manager->persist($blogPost);
        }
        $manager->flush();
    }
}
