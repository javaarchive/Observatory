import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management (basically remebers things once you change pages securely). You can generate random strings here:
# https://randomkeygen.com/
# smash your keyboard to make a key
SECRET_KEY = '~*VygALBXRB/.1G-IktDc9a^+z&T:]XenM1<wI%[Gq-?mHo5e1*[Dx%Qsia#_=wefrhuirfwruweyuwiyeruweryiweyure'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
