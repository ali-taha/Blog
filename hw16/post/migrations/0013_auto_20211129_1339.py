# Generated by Django 3.2.9 on 2021-11-29 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0012_auto_20211129_1333'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['title']},
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='tittle',
            new_name='title',
        ),
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
