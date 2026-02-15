from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title
