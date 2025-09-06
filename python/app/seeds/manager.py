"""
Seeder manager for orchestrating all seeders
"""
from .base import SeederRegistry
from .users import UserSeeder
from .posts import PostSeeder  
from .comments import CommentSeeder
from app.database.connection import get_session_local, Base, get_engine
import logging

logger = logging.getLogger(__name__)


class SeedManager:
    """Manager for database seeding operations"""
    
    def __init__(self, db=None):
        if db is None:
            SessionLocal = get_session_local()
            self.db = SessionLocal()
            self._external_db = False
        else:
            # Handle both session instances and sessionmaker
            if hasattr(db, 'query'):
                # Already a session
                self.db = db
            else:
                # Assume it's a sessionmaker
                self.db = db()
            self._external_db = True
        self.registry = SeederRegistry()
        self._register_seeders()
    
    def _register_seeders(self):
        """Register all seeders in dependency order"""
        self.registry.register(UserSeeder(self.db))
        self.registry.register(PostSeeder(self.db))
        self.registry.register(CommentSeeder(self.db))
    
    def seed_up(self):
        """Run all seeders (idempotent)"""
        try:
            logger.info("Starting database seeding...")
            
            # Ensure tables exist
            engine = get_engine()
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables ensured")
            
            # Run seeders
            self.registry.seed_all()
            
            logger.info("✅ Database seeding completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database seeding failed: {e}")
            self.db.rollback()
            raise
        finally:
            # Only close if we created the session
            if not self._external_db:
                self.db.close()
    
    def seed_down(self):
        """Clear all seeded data"""
        try:
            logger.info("Starting database clearing...")
            
            # Clear seeders in reverse order
            self.registry.clear_all()
            
            logger.info("✅ Database clearing completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database clearing failed: {e}")
            self.db.rollback()
            raise
        finally:
            if not self._external_db:
                self.db.close()
    
    def seed_reset(self):
        """Clear and re-seed all data"""
        logger.info("Starting database reset...")
        self.seed_down()
        
        # Create new session for seeding
        if not self._external_db:
            SessionLocal = get_session_local()
            self.db = SessionLocal()
        self._register_seeders()
        
        return self.seed_up()
    
    def seed_demo(self):
        """Seed with additional demo data"""
        logger.info("Starting demo seeding...")
        # For now, demo is the same as regular seeding
        # In the future, this could include more extensive demo data
        return self.seed_up()


def get_seed_manager(db=None):
    """Get a new instance of SeedManager"""
    return SeedManager(db)
