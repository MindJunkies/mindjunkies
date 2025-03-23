import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

from config.models import BaseModel


class UserManager(BaseUserManager):
    """Custom user manager with support for emails as unique identifiers."""

    @classmethod
    def normalize_email(cls, email):
        return super().normalize_email(email)

    def create_user(self, username, email, password=None, **extra_fields):
        """Creates and returns a regular user with the given details."""
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Creates and returns a superuser with admin privileges."""
        extra_fields.update({"is_staff": True, "is_superuser": True})
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with UUID primary key."""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.username} - {self.email}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class Profile(BaseModel):
    """User profile model storing additional user details."""

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile")
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    avatar = CloudinaryField(folder="avatars", overwrite=True, resource_type="image", null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
