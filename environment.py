import os

def select_env():
    if os.environ.get('APP_SETTING') == "production":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "authors.settings.production")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "authors.settings.development")
