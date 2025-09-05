# Test Suite for SF5 Blog Application

This test suite provides comprehensive unit and integration tests for the Symfony 7.3 blog application.

## Test Structure

### Entity Tests (`tests/Entity/`)
- **UserTest.php**: Tests for User entity including getters/setters, UserInterface implementation, and collection initialization
- **BlogPostTest.php**: Tests for BlogPost entity including relationships, interfaces, and date handling
- **CommentTest.php**: Tests for Comment entity including relationships and validation

### Event Subscriber Tests (`tests/EventSubscriber/`)
- **AuthoredEntitySubscriberTest.php**: Tests for automatic author assignment on POST requests
- **PublishedDateEntitySubscriberTest.php**: Tests for automatic published date setting on POST requests

### Controller Tests (`tests/Controller/`)
- **BlogControllerTest.php**: Functional tests for blog endpoints including list, get by ID/slug, add, and delete operations

### Repository Tests (`tests/Repository/`)
- **UserRepositoryTest.php**: Tests for UserRepository including CRUD operations and custom queries
- **BlogPostRepositoryTest.php**: Tests for BlogPostRepository including relationship queries and data persistence

### Integration Tests (`tests/Integration/`)
- **EntityRelationshipTest.php**: Tests to verify entity relationships, interface implementations, and validation requirements work correctly across the application

## Running Tests

Once dependencies are properly installed, run the tests using:

```bash
# Run all tests
php bin/phpunit

# Run specific test suite
php bin/phpunit tests/Entity/
php bin/phpunit tests/EventSubscriber/
php bin/phpunit tests/Controller/
php bin/phpunit tests/Repository/
php bin/phpunit tests/Integration/

# Run with coverage (if xdebug is enabled)
php bin/phpunit --coverage-html coverage/
```

## Test Coverage

The test suite covers:

1. **Entity Logic**:
   - Getters and setters
   - Fluent interfaces
   - Collection initialization
   - Interface implementations
   - Validation constraints

2. **Event Subscribers**:
   - Event subscription configuration
   - Conditional logic based on HTTP methods
   - User authentication and author assignment
   - Automatic date setting

3. **Controllers**:
   - HTTP endpoints and routing
   - JSON response format
   - Authentication requirements
   - Error handling

4. **Repositories**:
   - Basic CRUD operations
   - Custom query methods
   - Entity persistence
   - Relationship handling

5. **Integration**:
   - Entity relationships
   - Cross-component functionality
   - Validation requirements
   - Interface contracts

## Dependencies

The test suite requires:
- PHPUnit 12.x
- Symfony Test Framework
- Doctrine Test Bundle
- PHP 8.3+

## Notes

- Tests use mocking for external dependencies where appropriate
- Database tests use transaction rollback for cleanup
- Functional tests boot the Symfony kernel for realistic testing
- All tests follow PHPUnit best practices and naming conventions