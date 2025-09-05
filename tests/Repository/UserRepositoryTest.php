<?php

namespace App\Tests\Repository;

use App\Entity\User;
use App\Repository\UserRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

class UserRepositoryTest extends KernelTestCase
{
    private EntityManagerInterface $entityManager;
    private UserRepository $userRepository;

    protected function setUp(): void
    {
        $kernel = self::bootKernel();
        $this->entityManager = $kernel->getContainer()
            ->get('doctrine')
            ->getManager();
            
        $this->userRepository = $this->entityManager->getRepository(User::class);
    }

    protected function tearDown(): void
    {
        parent::tearDown();
        $this->entityManager->close();
        $this->entityManager = null;
    }

    public function testRepositoryIsInstanceOfServiceEntityRepository(): void
    {
        $this->assertInstanceOf(UserRepository::class, $this->userRepository);
    }

    public function testFindAllReturnsArray(): void
    {
        $users = $this->userRepository->findAll();
        $this->assertIsArray($users);
    }

    public function testFindByReturnsArray(): void
    {
        $users = $this->userRepository->findBy([]);
        $this->assertIsArray($users);
    }

    public function testFindOneByReturnsUserOrNull(): void
    {
        $user = $this->userRepository->findOneBy(['username' => 'non-existent-user']);
        $this->assertNull($user);
    }

    public function testFindReturnsUserOrNull(): void
    {
        $user = $this->userRepository->find(999999);
        $this->assertNull($user);
    }

    public function testRepositoryCanPersistAndFind(): void
    {
        $user = new User();
        $user->setUsername('testuser123');
        $user->setPassword('TestPassword123');
        $user->setName('Test User');
        $user->setEmail('test@example.com');
        $user->setRetypedPassword('TestPassword123');

        $this->entityManager->persist($user);
        $this->entityManager->flush();

        $foundUser = $this->userRepository->findOneBy(['username' => 'testuser123']);
        
        $this->assertNotNull($foundUser);
        $this->assertEquals('testuser123', $foundUser->getUsername());
        $this->assertEquals('Test User', $foundUser->getName());
        $this->assertEquals('test@example.com', $foundUser->getEmail());

        // Cleanup
        $this->entityManager->remove($foundUser);
        $this->entityManager->flush();
    }

    public function testRepositoryCountWorksCorrectly(): void
    {
        $initialCount = count($this->userRepository->findAll());
        
        $user = new User();
        $user->setUsername('counttest');
        $user->setPassword('TestPassword123');
        $user->setName('Count Test');
        $user->setEmail('count@test.com');
        $user->setRetypedPassword('TestPassword123');

        $this->entityManager->persist($user);
        $this->entityManager->flush();

        $newCount = count($this->userRepository->findAll());
        $this->assertEquals($initialCount + 1, $newCount);

        // Cleanup
        $this->entityManager->remove($user);
        $this->entityManager->flush();
    }
}