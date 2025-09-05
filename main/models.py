from django.db import models

# Create your models here.
import uuid
from django.db import models

class News(models.Model):
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

    #  name sebagai nama item dengan tipe CharField.
    #  price sebagai harga item dengan tipe IntegerField.
    #  description sebagai deskripsi item dengan tipe TextField.
    #  thumbnail sebagai gambar item dengan tipe URLField.
    #  category sebagai kategori item dengan tipe CharField.
    #  is_featured sebagai status unggulan item dengan tipe BooleanField.
    
    def __str__(self):
        return self.title
    
    @property
    def is_news_hot(self):
        return self.news_views > 20
        
    def increment_views(self):
        self.news_views += 1
        self.save()