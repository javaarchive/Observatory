import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management (basically remebers things once you change pages securely). You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = os.environ.get("SECRET");

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db') # put our database in the current directory
