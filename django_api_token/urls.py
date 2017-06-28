from django.conf.urls import url

import django_api_token.views

urlpatterns = [
    # The admin urls and the standard index page url
    url(r'^token', django_api_token.views.token, name='token'),
]
