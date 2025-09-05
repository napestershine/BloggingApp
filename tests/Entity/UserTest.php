<?php

namespace App\Tests\Entity;

use App\Entity\User;
use PHPUnit\Framework\TestCase;

class UserTest extends TestCase
{
    private User $user;

    protected function setUp(): void
    {
        $this->user = new User();
    }

    public function testGettersAndSetters(): void
    {
        $username = 'testuser';
        $password = 'TestPassword123';
        $name = 'Test User';
        $email = 'test@example.com';
        $retypedPassword = 'TestPassword123';

        $this->user->setUsername($username);
        $this->user->setPassword($password);
        $this->user->setName($name);
        $this->user->setEmail($email);
        $this->user->setRetypedPassword($retypedPassword);

        $this->assertEquals($username, $this->user->getUsername());
        $this->assertEquals($password, $this->user->getPassword());
        $this->assertEquals($name, $this->user->getName());
        $this->assertEquals($email, $this->user->getEmail());
        $this->assertEquals($retypedPassword, $this->user->getRetypedPassword());
    }

    public function testUserInterface(): void
    {
        $username = 'testuser';
        $this->user->setUsername($username);

        $this->assertEquals($username, $this->user->getUserIdentifier());
        $this->assertEquals(['ROLE_USER'], $this->user->getRoles());
        $this->assertNull($this->user->getSalt());
    }

    public function testCollectionsInitialization(): void
    {
        $this->assertCount(0, $this->user->getPosts());
        $this->assertCount(0, $this->user->getComments());
    }

    public function testIdIsNullByDefault(): void
    {
        $this->assertNull($this->user->getId());
    }

    public function testEraseCredentials(): void
    {
        // Should not throw an exception
        $this->user->eraseCredentials();
        $this->assertTrue(true);
    }

    public function testFluentInterface(): void
    {
        $result = $this->user->setUsername('test')
            ->setPassword('Test123')
            ->setName('Test')
            ->setEmail('test@test.com');

        $this->assertSame($this->user, $result);
    }
}