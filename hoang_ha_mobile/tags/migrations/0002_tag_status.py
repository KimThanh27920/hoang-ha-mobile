# Generated by Django 4.0.4 on 2022-07-26 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]