from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models import BaseModel
from taxonomy.models import Categories, Tags
from taxonomy.utils import generate_unique_slug
from articles.models import Author, Source

class Article(BaseModel):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING_REVIEW = "pending_review", "Pending Review"
        PUBLISHED = "published", "Published"
        SCHEDULED = "scheduled", "Scheduled"
        ARCHIVED = "archived", "Archived"

    # ---------- Core content ----------
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    short_description = models.TextField(blank=True, null=True, help_text="Short summary shown in listings/previews")
    content = models.TextField(help_text="Full rich HTML article content")

    # ---------- Media ----------
    featured_image = models.ImageField(upload_to="articles/featured/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="articles/thumbnails/", blank=True, null=True)

    # ---------- Relations ----------
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name="articles")
    tags = models.ManyToManyField(Tags, blank=True, related_name="articles")
    authors = models.ManyToManyField(Author, blank=True, related_name="articles")
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, blank=True, null=True, related_name="articles")
    related_articles = models.ManyToManyField("self", blank=True)

    # ---------- Publishing ----------
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    publish_date = models.DateTimeField(blank=True, null=True)
    schedule_date = models.DateTimeField(blank=True, null=True)

    # ---------- Flags ----------
    is_featured = models.BooleanField(default=False)
    is_breaking_news = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_editors_pick = models.BooleanField(default=False)

    # ---------- Engagement ----------
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    # ---------- Reading time (minutes) ----------
    reading_time = models.PositiveIntegerField(default=1)

    # ---------- SEO ----------
    seo_title = models.CharField(max_length=200, blank=True, null=True)
    seo_description = models.CharField(max_length=300, blank=True, null=True)
    focus_keyword = models.CharField(max_length=150, blank=True, null=True)
    canonical_url = models.URLField(blank=True, null=True)
    og_image = models.ImageField(upload_to="articles/og/", blank=True, null=True)
    twitter_image = models.ImageField(upload_to="articles/twitter/", blank=True, null=True)

    class Meta:
        db_table = 'ARTICLES'
        ordering = ["-publish_date", "-entry_on"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Article, self.title, instance_pk=self.pk)

        if self.status == self.Status.PUBLISHED and not self.publish_date:
            self.publish_date = timezone.now()

        if self.content:
            word_count = len(self.content.split())
            self.reading_time = max(1, round(word_count / 200))

        super().save(*args, **kwargs)