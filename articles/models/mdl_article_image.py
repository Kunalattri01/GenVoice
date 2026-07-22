from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models import BaseModel
from taxonomy.models import Categories, Tags
from taxonomy.utils import generate_unique_slug
from articles.models import Article

class ArticleImage(BaseModel):
    """Gallery images attached to an article."""

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="articles/gallery/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'ARTICLE_IMAGES'
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.article.title} — image {self.display_order}"