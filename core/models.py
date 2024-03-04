from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from core.manager import CustomUserManager
from django.utils import timezone
import uuid
class User(AbstractUser):
    profile_pic = models.ImageField(upload_to="usr/pics", null=True, default="")
    first_name = models.CharField(max_length=100, default='', null=True)
    last_name = models.CharField(max_length=100, default='', null=True)
    age = models.IntegerField(default=0, null=True)
    address = models.TextField(default=None, null=True)

    username = models.CharField(max_length = 100, null=True, blank=True)
    email = models.EmailField(_("email address"), null=False, unique=True)
    last_login = models.DateTimeField(default=None, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', blank=True)

    


class ListApp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    description = models.TextField(default='')
    image_a = models.ImageField(upload_to="listimage", default=None, null=True)
    image_b = models.ImageField(upload_to="listimage", default=None, null=True)
    mark_as_completed = models.BooleanField(default=False, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)  # Provide a default value

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set date_created on creation, not update
            self.date_created = timezone.now()
        super().save(*args, **kwargs)

        def __str__(self):
            return self.title
        

class Prefdefinelist(models.Model):
    title = models.CharField(max_length=200, default="")
    description = models.TextField(default='', null=True)
    image_a = models.ImageField(upload_to="listimage", default=None, null=True)
    image_b = models.ImageField(upload_to="listimage", default=None, null=True)
    mark_as_completed = models.BooleanField(default=False, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    


class SocialPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(default='', null=True)
    image_a = models.ImageField(upload_to="social/post", default=None, null=True)
    image_b = models.ImageField(upload_to="social/post", default=None, null=True)
    date_created = models.DateTimeField(default=timezone.now)  # Provide a default value
    slug = models.SlugField(unique=True, default="")
    is_trending = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_created = timezone.now()
            self.slug = uuid.uuid4()  # This generates a UUID string, not a slug
        super().save(*args, **kwargs)
