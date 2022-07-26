# Generated by Django 4.0.4 on 2022-07-25 09:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]
