import os
import sys


def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    global_settings.INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.sites',
        'django.contrib.contenttypes',
        'webcommands',
    )
    global_settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    global_settings.MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    )
    global_settings.SECRET_KEY = "secret_key_for_testing"

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)
    test_runner = test_runner()
    failures = test_runner.run_tests(['webcommands'])
    sys.exit(failures)

if __name__ == '__main__':
    main()
