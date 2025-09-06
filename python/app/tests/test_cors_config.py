"""
Test CORS configuration parsing
"""
import pytest
import os
from unittest.mock import patch
from app.core.config import Settings


def test_cors_origins_comma_separated_string():
    """Test that CORS origins can be parsed from comma-separated string"""
    with patch.dict(os.environ, {
        'DATABASE_URL': 'sqlite:///test.db',
        'CORS_ORIGINS': 'http://localhost:3000,http://web:3000,https://example.com'
    }):
        settings = Settings()
        expected = ['http://localhost:3000', 'http://web:3000', 'https://example.com']
        assert settings.cors_origins_list == expected


def test_cors_origins_with_spaces():
    """Test that CORS origins handles spaces around commas"""
    with patch.dict(os.environ, {
        'DATABASE_URL': 'sqlite:///test.db',
        'CORS_ORIGINS': 'http://localhost:3000, http://web:3000 , https://example.com'
    }):
        settings = Settings()
        expected = ['http://localhost:3000', 'http://web:3000', 'https://example.com']
        assert settings.cors_origins_list == expected


def test_cors_origins_single_value():
    """Test that CORS origins works with single value"""
    with patch.dict(os.environ, {
        'DATABASE_URL': 'sqlite:///test.db',
        'CORS_ORIGINS': 'http://localhost:3000'
    }):
        settings = Settings()
        expected = ['http://localhost:3000']
        assert settings.cors_origins_list == expected


def test_cors_origins_empty_values_filtered():
    """Test that empty values are filtered out"""
    with patch.dict(os.environ, {
        'DATABASE_URL': 'sqlite:///test.db',
        'CORS_ORIGINS': 'http://localhost:3000,,http://web:3000,'
    }):
        settings = Settings()
        expected = ['http://localhost:3000', 'http://web:3000']
        assert settings.cors_origins_list == expected


def test_cors_origins_default_value():
    """Test default CORS origins when environment variable not set"""
    with patch.dict(os.environ, {
        'DATABASE_URL': 'sqlite:///test.db'
    }, clear=True):
        # Clear CORS_ORIGINS if it exists
        if 'CORS_ORIGINS' in os.environ:
            del os.environ['CORS_ORIGINS']
        
        settings = Settings()
        expected = ['http://localhost:3000', 'http://localhost:8080']
        assert settings.cors_origins_list == expected