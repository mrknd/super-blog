from django.contrib import admin

from .models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'updated_at', 'status']
    list_display_links = ['title', 'author']
    list_filter = ['status', 'updated_at', 'publish', 'author']

    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'body']
    # raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['-updated_at', 'status', '-publish']
    show_facets = admin.ShowFacets.ALWAYS


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['name', 'email', 'post', 'created_at', 'active']
#     list_filter = ['active', 'created_at']
#     search_fields = ['name', 'email', 'body']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'created_at', 'updated_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'comment', 'created_at', 'updated_at']
    list_display_links = ['id', 'user']
