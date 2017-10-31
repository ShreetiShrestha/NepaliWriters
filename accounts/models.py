from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import datetime

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic=models.ImageField(upload_to='profile_images')

    def __str__(self):
        return (self.username)

class Category(models.Model):
    name=models.CharField(max_length=50)
    no_of_post=models.IntegerField(default=0)
    category_image= models.ImageField(upload_to='categories_images')
    def __str__(self):
        return str(self.name)

class Post(models.Model):
    title=models.CharField(max_length=100)
    caption = models.CharField(max_length=200,blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,blank=False)
    description = models.TextField(null=True, blank=True)
    image= models.ImageField(upload_to='post_images',blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    no_of_like=models.IntegerField(default=0)
    no_of_comment=models.IntegerField(default=0)
    def __str__(self):
        return str(self.title)

class Comment(models.Model):
    commentor=models.ForeignKey(settings.AUTH_USER_MODEL,blank=False)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    time=models.DateTimeField(default=datetime.datetime.now())

class PostToReview(models.Model):
    title=models.CharField(max_length=100)
    caption = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,blank=False)
    description = models.TextField(null=True, blank=True)
    image= models.ImageField(upload_to='post_images',blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    no_of_like=models.IntegerField(default=0)
    no_of_comment=models.IntegerField(default=0)
    status=models.BooleanField(default=False)
    def __str__(self):
        return str(self.title)
# Create your models here.
