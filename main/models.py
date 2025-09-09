from django.db import models

# Create your models here.
import uuid
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('historic', 'Historic'),
        ('exclusive', 'Exclusive'),
        ('fan', 'Fan'),
        ('misc', 'Miscellanous'),
    ]
    
    name = models.CharField()
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField()
    likes = models.IntegerField()
    
    def __str__(self):
        return self.name
    
    @property
    def is_product_trending(self):
        return self.likes > 100
        
    def increment_likes(self):
        self.news_views += 1
        self.save()