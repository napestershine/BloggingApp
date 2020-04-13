<?php

declare(strict_types=1);

namespace App\DataFixtures;

use App\Entity\BlogPost;
use App\Entity\Comment;
use App\Entity\User;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Common\Persistence\ObjectManager;
use Symfony\Component\Security\Core\Encoder\UserPasswordEncoderInterface;
use Symfony\Component\String\Slugger\AsciiSlugger;
use Symfony\Component\String\Slugger\SluggerInterface;

/**
 * Class AppFixtures
 * @package App\DataFixtures
 */
class AppFixtures extends Fixture
{
    private const USERS = [
        [
            'username' => 'admin',
            'email' => 'admin@blog.com',
            'name' => 'Admin',
            'password' => 'Admin123'
        ],
        [
            'username' => 'editor',
            'email' => 'editor@blog.com',
            'name' => 'Editor',
            'password' => 'Editor123'
        ],
        [
            'username' => 'author',
            'email' => 'author@blog.com',
            'name' => 'Author',
            'password' => 'Author123'
        ],
        [
            'username' => 'subscriber',
            'email' => 'subscriber@blog.com',
            'name' => 'Subscriber',
            'password' => 'Subscriber123'
        ]
    ];

    /**
     * @var UserPasswordEncoderInterface
     */
    private $userPasswordEncoder;

    /**
     * @var \Faker\Factory
     */
    private $faker;

    /**
     * @var SluggerInterface
     */
    private $slugger;

    /**
     * AppFixtures constructor.
     * @param UserPasswordEncoderInterface $userPasswordEncoder
     */
    public function __construct(UserPasswordEncoderInterface $userPasswordEncoder, SluggerInterface $slugger)
    {
        $this->userPasswordEncoder = $userPasswordEncoder;
        $this->faker = \Faker\Factory::create();
        $this->slugger = $slugger;
    }

    /**
     * @param ObjectManager $manager
     * @throws \Exception
     */
    public function load(ObjectManager $manager)
    {
        $this->loadUsers($manager);
        $this->loadBlogPosts($manager);
        $this->loadComments($manager);
    }

    /**
     * @param ObjectManager $manager
     * @throws \Exception
     */
    public function loadBlogPosts(ObjectManager $manager)
    {
        $user = $this->getReference('user_admin');
        for ($i = 0; $i < 100; $i++) {
            $blogPost = new BlogPost();
            $title = $this->faker->realText(30);
            $blogPost->setTitle($title)
                ->setPublished($this->faker->dateTimeThisYear)
                ->setContent($this->faker->realText())
                ->setSlug($this->slugger->slug($title)->toString());

            $authorReference = $this->getRandomUserReference();
            $blogPost->setAuthor($authorReference);

            $this->setReference("blog_post_$i", $blogPost);
            $manager->persist($blogPost);
        }

        $manager->flush();
    }

    /**
     * @param ObjectManager $manager
     */
    public function loadComments(ObjectManager $manager)
    {
        for ($i = 0; $i < 100; $i++) {
            for ($j = 0; $j < rand(1, 10); $j++) {
                $comment = new Comment();
                $comment->setContent($this->faker->realText())
                    ->setPublished($this->faker->dateTimeThisYear);

                $authorReference = $this->getRandomUserReference();
                $comment->setAuthor($authorReference);
                $comment->setBlogPost($this->getReference("blog_post_$i"));
                $manager->persist($comment);
            }
        }
        $manager->flush();
    }

    /**
     * @param ObjectManager $manager
     */
    public function loadUsers(ObjectManager $manager)
    {
        foreach (self::USERS as $userFixture) {
            $user = new User();
            $user->setUsername($userFixture['username'])
                ->setEmail($userFixture['email'])
                ->setName($userFixture['name']);

            $user->setPassword($this->userPasswordEncoder->encodePassword($user, $userFixture['password']));

            $this->addReference('user_' . $userFixture['username'], $user);
            $manager->persist($user);
        }
        $manager->flush();
    }

    /**
     * @return object
     */
    private function getRandomUserReference(): object
    {
        return $this->getReference('user_' . self::USERS[rand(0, 3)]['username']);
    }
}
