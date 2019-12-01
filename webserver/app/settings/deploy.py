from .base import *

# override the settings from base.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        
        # 'NAME': os.getenv('POSTGRES_DB'),
        # 'USER': os.getenv('POSTGRES_USER'),
        # 'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        # 'HOST': os.getenv('DB_HOST'),
        # 'PORT': os.getenv('DB_PORT'),

        'NAME': 'scriptdb',
        'USER': 'script_admin',
        'PASSWORD': 'script_passwd',
        'HOST': 'script-postgresql-db.cfnv951vt1nj.us-east-1.rds.amazonaws.com',
        'PORT': 5432,
    }
}
