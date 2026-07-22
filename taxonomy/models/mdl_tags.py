from django.db import models

from core.models import BaseModel
from taxonomy.utils import generate_unique_slug


class Tags(BaseModel):

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=130, unique=True, blank=True)

    class Meta:
        db_table = 'TAGS'
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = generate_unique_slug(Tags, self.name)
        elif self._slug_source_changed():
            self.slug = generate_unique_slug(Tags, self.name, instance_pk=self.pk)
        super().save(*args, **kwargs)
        

    def _slug_source_changed(self):
        """
            Returns True if `name` has changed compared to the DB value,
            so the slug is only regenerated when necessary.
        """
        old = Tags.objects.filter(pk=self.pk).values_list("name", flat=True).first()
        return old is not None and old != self.name