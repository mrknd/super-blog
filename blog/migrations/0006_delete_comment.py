# Generated by Django 5.0.6 on 2024-06-11 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
