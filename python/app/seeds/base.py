"""
Base seeder class providing common functionality for all seeders
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class BaseSeeder(ABC):
    """Base class for all database seeders"""
    
    def __init__(self, db: Session):
        self.db = db
    
    @abstractmethod
    def seed(self) -> None:
        """Implement this method to define seeding logic"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Implement this method to define clearing logic"""
        pass
    
    def get_or_create(self, model_class, defaults: Optional[Dict[str, Any]] = None, **kwargs):
        """
        Get an existing record or create a new one.
        Returns (instance, created) where created is a boolean.
        """
        instance = self.db.query(model_class).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            params = dict(kwargs)
            if defaults:
                params.update(defaults)
            instance = model_class(**params)
            try:
                self.db.add(instance)
                self.db.commit()
                self.db.refresh(instance)
                return instance, True
            except IntegrityError:
                self.db.rollback()
                instance = self.db.query(model_class).filter_by(**kwargs).first()
                return instance, False
    
    def safe_commit(self):
        """Safely commit changes with rollback on error"""
        try:
            self.db.commit()
            return True
        except IntegrityError as e:
            logger.error(f"Integrity error during seeding: {e}")
            self.db.rollback()
            return False
        except Exception as e:
            logger.error(f"Unexpected error during seeding: {e}")
            self.db.rollback()
            raise


class SeederRegistry:
    """Registry to manage all seeders"""
    
    def __init__(self):
        self._seeders: List[BaseSeeder] = []
    
    def register(self, seeder: BaseSeeder):
        """Register a seeder"""
        self._seeders.append(seeder)
    
    def seed_all(self):
        """Run all registered seeders"""
        for seeder in self._seeders:
            logger.info(f"Running seeder: {seeder.__class__.__name__}")
            seeder.seed()
    
    def clear_all(self):
        """Clear all seeded data (in reverse order)"""
        for seeder in reversed(self._seeders):
            logger.info(f"Clearing seeder: {seeder.__class__.__name__}")
            seeder.clear()
