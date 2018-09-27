import dj_database_url
import django_heroku

from .defaults import *

# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

DEBUG = config('DEBUG', cast=bool)
django_heroku.settings(locals(), test_runner=False)
DATABASES = {
    'default': {}
}
DATABASES["default"]=dj_database_url.config(default=os.environ.get("DATABASE_URL", None))

