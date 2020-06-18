from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail

class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')
    nickname = models.CharField(max_length=50, unique=True, default=datetime.now())
    intro = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(blank=True, upload_to="profile/%Y/%m/%d", default='images/custom_no_image.jpg')
    image_thumbnail = ImageSpecField(source='photo',
                        processors=[Thumbnail(150, 150)],
                        format='JPEG',
                        options={'quality': 90})