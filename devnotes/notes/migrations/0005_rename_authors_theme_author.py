# Generated by Django 4.1.2 on 2022-10-14 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_remove_theme_author_theme_authors_alter_note_author_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='theme',
            old_name='authors',
            new_name='author',
        ),
    ]
