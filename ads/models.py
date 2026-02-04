from django.db import models

from users.models import User


# Create your models here.
class Ad(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.creator.id) + " " + self.title
