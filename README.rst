====================
Django API Token
====================

This app allows to call an endpoint to generate an API token that subsequently can be used to interact with an API

Quick start
-----------

1. Add "django_api_token" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_api_token',
    ]

2. Include the django_api_token URLconf in your project urls.py like this::

    url(r'^', include('django_api_token.urls')),

3. Run `python manage.py migrate` to create the django_api_token models.

4. Configure the settings.py to set the configurations for
    * DJANGO_API_TOKEN_LIFESPAN = 3600
