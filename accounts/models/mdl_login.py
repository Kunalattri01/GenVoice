from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ("ADMIN", "ADMIN"),
        ("EDITOR", "EDITOR"),
        ("REPORTER", "REPORTER"),
    )

    id = models.AutoField(primary_key=True, db_column='ID')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="REPORTER", db_column='ROLE')
    profile_image = models.ImageField(upload_to="users/", blank=True, null=True, db_column='PROFILE_IMAGE')
    phone_number = models.CharField(max_length=15, blank=True, db_column='PHONE_NUMBER')
    is_verified = models.BooleanField(default=True, db_column='IS_VERIFIED')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    updated_at = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        
        db_table = 'USER_MT'
        ordering = ["-created_at"]

    def __str__(self):
        return self.get_full_name() or self.username