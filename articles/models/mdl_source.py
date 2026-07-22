from django.db import models

from core.models import BaseModel

class Source(BaseModel):
    """External/original publication source, used for attribution only."""

    name = models.CharField(max_length=150, unique=True)
    url = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="sources/logos/", blank=True, null=True)

    class Meta:
        db_table = 'SOURCES'
        ordering = ["name"]

    def __str__(self):
        return self.name