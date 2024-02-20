from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from core.manager import CustomUserManager
from django.utils import timezone

class User(AbstractUser):
    username = models.CharField(max_length = 100, null=True, blank=True)
    full_name = models.CharField(max_length=100, default='')
    email = models.EmailField(_("email address"), null=False, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=None, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', blank=True)


class ListApp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    description = models.TextField(default='')
    image_a = models.ImageField(upload_to="listimage", default=None)
    image_b = models.ImageField(upload_to="listimage", default=None)
    mark_as_completed = models.BooleanField(default=False, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)  # Provide a default value

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set date_created on creation, not update
            self.date_created = timezone.now()
        super().save(*args, **kwargs)