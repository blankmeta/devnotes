# Generated by Django 4.1.2 on 2022-10-12 18:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notes',
            new_name='Note',
        ),
        migrations.RenameModel(
            old_name='Themes',
            new_name='Theme',
        ),
    ]
