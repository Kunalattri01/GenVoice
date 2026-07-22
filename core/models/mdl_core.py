from django.conf import settings
from django.db import models

class BaseModel(models.Model):

    id = models.BigAutoField(primary_key=True, db_column='id')
    entry_on = models.DateTimeField(auto_now_add=True, db_column='entry_on')
    entry_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="+", db_column='entry_by')
    updated_on = models.DateTimeField(auto_now=True, db_column='updated_on')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="+", db_column='updated_by')
    is_active = models.BooleanField(default=True, db_column='is_active')

    class Meta:
        abstract = True
        ordering = ["-entry_on"]