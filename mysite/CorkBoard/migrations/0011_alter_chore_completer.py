# Generated by Django 5.1.1 on 2024-09-27 07:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CorkBoard', '0010_chore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='completer',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='completer', to='CorkBoard.users'),
        ),
    ]
