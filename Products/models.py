from django.db import models
from django.template.defaultfilters import slugify
import uuid

class Tag(models.Model):
    caption = models.CharField(max_length=20)
    def __str__(self):
        return self.caption

class Product(models.Model):
    name = models.CharField(max_length=50, null=False)
    slug = models.SlugField(null=False, blank=False, unique=True)
    price = models.IntegerField(null=False)
    description = models.TextField(null=False)
    excerpt = models.CharField(max_length=150, default='')
    image = models.ImageField(upload_to="images")
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return f"{self.name} costs {self.price}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
       