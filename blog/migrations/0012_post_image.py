# Generated by Django 5.0.6 on 2024-06-12 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_post_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default=1, upload_to='blog_posts_image'),
            preserve_default=False,
        ),
    ]