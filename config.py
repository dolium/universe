"""
Configuration module for UniVerse application.
Centralizes all configuration values and constants.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration class with common settings."""

    # Application Settings
    APP_NAME = os.getenv('SITE_NAME', 'UniVerse')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-me')

    # Google Analytics
    GOOGLE_ANALYTICS_ID = os.getenv('GA_MEASUREMENT_ID', '')

    # Google Sheets Configuration
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
    GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')

    # Worksheet Names
    COURSES_WORKSHEET_NAME = 'Courses'
    MATERIALS_WORKSHEET_NAME = os.getenv('MATERIALS_SHEET_NAME', 'Materials')
    OPPORTUNITIES_WORKSHEET_NAME = os.getenv('OPPORTUNITIES_SHEET_NAME', 'Opportunities')
    TIMETABLE_WORKSHEET_NAME = os.getenv('TIMETABLE_SHEET_NAME', 'Timetable')

    # External URLs for Adding Data
    ADD_MATERIAL_SHEET_URL = "https://docs.google.com/spreadsheets/d/1-bH05NhyJ1WFOcrmX0BtVVuvd4wWX4jx8VB-AYrOdQY/edit?gid=935728683#gid=935728683"
    ADD_OPPORTUNITY_SHEET_URL = "https://docs.google.com/spreadsheets/d/1-bH05NhyJ1WFOcrmX0BtVVuvd4wWX4jx8VB-AYrOdQY/edit?gid=998865460#gid=998865460"


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing-specific configuration."""
    DEBUG = True
    TESTING = True


# Configuration dictionary for easy access
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(environment_name: str = None):
    """
    Get configuration object based on environment name.

    Args:
        environment_name: Name of the environment (development, production, testing)

    Returns:
        Configuration class for the specified environment
    """
    if environment_name is None:
        environment_name = os.getenv('FLASK_ENV', 'development')

    return config_by_name.get(environment_name, DevelopmentConfig)

