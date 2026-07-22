from django.db import models

from core.models import BaseModel
from taxonomy.utils import generate_unique_slug


class Categories(BaseModel):

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True, help_text="Example: fa-folder-open")
    icon_color = models.CharField(max_length=100, default="text-textsecondary", help_text="Tailwind class e.g. text-blue-500")
    display_order = models.PositiveIntegerField(default=0)

    seo_title = models.CharField(max_length=200, blank=True, null=True)
    seo_description = models.CharField(max_length=300, blank=True, null=True)
    seo_keywords = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'CATEGORIES'
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name



    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = generate_unique_slug(Categories, self.name)
        elif self._slug_source_changed():
            self.slug = generate_unique_slug(Categories, self.name, instance_pk=self.pk)
        super().save(*args, **kwargs)


    def _slug_source_changed(self):
        """
            Returns True if `name` has changed compared to the DB value,
            so the slug is only regenerated when necessary.
        """
        old = Categories.objects.filter(pk=self.pk).values_list("name", flat=True).first()
        return old is not None and old != self.name