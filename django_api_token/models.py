from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class Token(models.Model):
    user = models.OneToOneField(User)
    expires_at = models.DateTimeField(null=True, blank=True, help_text="When the token expires")
    token = models.CharField(default='', max_length=32, help_text="The token that is used after authentication")

