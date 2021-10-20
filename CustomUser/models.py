from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .custom_manager import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=200, unique=True)
    number = models.IntegerField()
    city = models.CharField(max_length=100, default='', null=False, blank=False)
    auth_token = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    username = None
    first_name = None
    last_name = None
    groups = None
    user_permissions = None
    last_login = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'number']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
