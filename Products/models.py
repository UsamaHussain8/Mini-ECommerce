from django.db import models
from django.template.defaultfilters import slugify


class Tag(models.Model):
    caption = models.CharField(max_length=20)
    def __str__(self):
        return self.caption

class Product(models.Model):
    name = models.CharField(max_length=50, null=False)
    slug = models.SlugField(null=False, blank=False, unique=True)
    price = models.IntegerField(null=False, default=1)
    description = models.TextField(null=False, default='')
    excerpt = models.CharField(max_length=150, default='', null=False)
    image = models.ImageField(upload_to="images", default="images/default.jpeg")
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return f"{self.name} costs {self.price}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)