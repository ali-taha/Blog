# Generated by Django 3.2.9 on 2021-12-04 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0017_alter_comment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(blank=True, default='SEO', null=True, to='post.Tag'),
        ),
    ]
