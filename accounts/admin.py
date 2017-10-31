from django.contrib import admin
from .models import *
from django.conf import settings
# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(PostToReview)