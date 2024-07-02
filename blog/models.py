from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

from ckeditor.fields import RichTextField


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    category_icon = models.ImageField(upload_to='category_icons')
    category_color = models.CharField(max_length=10, default='#00bd91')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category_name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = ('DF', 'Draft')
        PUBLISHED = ('PB', 'Published')

    objects = models.Manager()
    published = PublishedManager()

    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    short_description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='blog_posts_image')
    featured_image = models.ImageField(upload_to='blog_posts_featured_image', blank=True)
    body = RichTextField(blank=True, null=True)
    body2 = RichTextUploadingField(blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    tags = TaggableManager()
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def calculate_reading_time(self):
        words_per_minut = 150
        words = self.body.split()
        num_words = len(words)
        reading_time = num_words / words_per_minut
        if reading_time < 1:
            reading_time = 1
        return round(reading_time)


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')

    def __str__(self):
        return f"Image for post: {self.post.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    comment = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'
