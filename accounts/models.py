from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    is_verify = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    


class ProfileUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')

    birth_date = models.DateField(null=True)

    @property
    def fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"Profile for: {self.user.username}"

        

