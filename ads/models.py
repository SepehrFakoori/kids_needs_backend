from django.db import models

from accounts.models import User
from categories.models import Category


# Create your models here.
class Ad(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="ads",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.creator.username} | {self.title} | {self.created_at}"


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="ads/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for ad {self.ad.title}"
