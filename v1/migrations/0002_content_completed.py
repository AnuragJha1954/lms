# Generated by Django 4.2.5 on 2025-05-16 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
