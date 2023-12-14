from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    # additional fields required
    contact_details = models.TextField(max_length=250)
    address = models.TextField(max_length=250)

    def __repr__(self):
        return self.username
