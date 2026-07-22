from django.conf import settings
from django.db import models

from core.models import BaseModel
from taxonomy.utils import generate_unique_slug


class Author(BaseModel):
    """A byline author. Optionally linked to a staff User account."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="author_profile"
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="authors/avatars/", blank=True, null=True)
    designation = models.CharField(max_length=150, blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'AUTHORS'
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Author, self.name, instance_pk=self.pk)
        super().save(*args, **kwargs)