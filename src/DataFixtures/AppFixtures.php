<?php

declare(strict_types=1);

namespace App\DataFixtures;

use App\Entity\BlogPost;
use App\Entity\User;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Common\Persistence\ObjectManager;
use Symfony\Component\Security\Core\Encoder\UserPasswordEncoderInterface;

/**
 * Class AppFixtures
 * @package App\DataFixtures
 */
class AppFixtures extends Fixture
{
    /**
     * @var UserPasswordEncoderInterface
     */
    private $userPasswordEncoder;

    /**
     * AppFixtures constructor.
     * @param UserPasswordEncoderInterface $userPasswordEncoder
     */
    public function __construct(UserPasswordEncoderInterface $userPasswordEncoder)
    {
        $this->userPasswordEncoder = $userPasswordEncoder;
    }

    /**
     * @param ObjectManager $manager
     * @throws \Exception
     */
    public function load(ObjectManager $manager)
    {
        $this->loadUsers($manager);
        $this->loadBlogPosts($manager);

    }

    /**
     * @param ObjectManager $manager
     * @throws \Exception
     */
    public function loadBlogPosts(ObjectManager $manager)
    {
        $user = $this->getReference('user_admin');
        for ($i = 1; $i < 10; $i++) {
            $blogPost = new BlogPost();
            $blogPost->setTitle('this is post title ' . $i)
                ->setPublished(new \DateTime())
                ->setContent('This is content ' . $i)
                ->setSlug('slug-title-' . $i)
                ->setAuthor($user);
            $manager->persist($blogPost);
        }
        $manager->flush();
    }

    public function loadComments(ObjectManager $manager)
    {

    }

    /**
     * @param ObjectManager $manager
     */
    public function loadUsers(ObjectManager $manager)
    {
        $user = new User();
        $user->setUsername('admin')
            ->setEmail('admin@blog.com')
            ->setName('Manu');
        $user
            ->setPassword($this->userPasswordEncoder->encodePassword($user, '123'));

        $this->addReference('user_admin', $user);

        $manager->persist($user);
        $manager->flush();
    }
}
