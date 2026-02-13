from django.db import models


# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} >> {self.phone_number}"
