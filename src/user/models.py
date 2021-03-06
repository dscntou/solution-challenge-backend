import binascii
import os
import random

from django.db import models
from django.utils.translation import gettext_lazy as _


USER_ROLE = [
    ('null', _('null')),
    ('mentor', _('mentor')),
    ('mentee', _('mentee'))
]


class User(models.Model):
    token = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=8, choices=USER_ROLE, default='null')
    bio = models.TextField(blank=True)
    career = models.CharField(max_length=100, blank=True)
    verify = models.BooleanField(default=False)
    verify_code = models.CharField(max_length=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
        if not self.verify_code:
            self.verify_code = str(random.randrange(1000, 9999))
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.email
