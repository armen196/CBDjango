# Generated by Django 4.2.6 on 2024-09-06 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CorkBoard', '0005_remove_postsreplies_postid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='postID',
        ),
        migrations.AddField(
            model_name='postsreplies',
            name='postID',
            field=models.CharField(default='null', max_length=10),
            preserve_default=False,
        ),
    ]
