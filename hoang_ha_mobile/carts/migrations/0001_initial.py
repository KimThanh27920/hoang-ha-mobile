# Generated by Django 4.0.4 on 2022-07-19 06:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('variants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='variants.variant')),
            ],
            options={
                'db_table': 'carts',
            },
        ),
    ]