# Generated by Django 5.0.6 on 2024-06-19 18:16

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_post_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='body2',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]