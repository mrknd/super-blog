from django import template
from django.db.models import Count

from django.utils.safestring import mark_safe
import markdown

from taggit.models import Tag
from ..models import Post, Comment, Category


register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published().count()


@register.simple_tag
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    context = {
        'latest_posts': latest_posts
    }
    return context


@register.simple_tag
def get_latest_comments(count=3):
    return Comment.objects.order_by('-created_at')[:count]


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def get_display_pages(current_page, last_page, display_range=5):
    start_page = max(current_page - display_range//2, 1)
    end_page = min(start_page + display_range - 1, last_page)
    if end_page - start_page < display_range:
        start_page = max(end_page - display_range + 1, 1)
    return range(start_page, end_page + 1)


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag
def get_tags():
    return Tag.objects.all()


