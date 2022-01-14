import os
from team_companion.conf.settings import secret_key, postgresql_uri, debugging_enabled

# Define the application directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = "production"
SECRET_KEY = secret_key
DEBUG = debugging_enabled

# Database configuration
SQLALCHEMY_DATABASE_URI = postgresql_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False