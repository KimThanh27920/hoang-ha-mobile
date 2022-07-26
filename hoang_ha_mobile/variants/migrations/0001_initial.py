# Generated by Django 4.0.4 on 2022-07-26 01:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255)),
                ('size', models.CharField(blank=True, max_length=255, null=True)),
                ('strap', models.CharField(blank=True, max_length=255, null=True)),
                ('general', models.CharField(blank=True, max_length=255, null=True)),
                ('utilities', models.CharField(blank=True, max_length=255, null=True)),
                ('network', models.CharField(blank=True, max_length=255, null=True)),
                ('storage', models.CharField(blank=True, max_length=255, null=True)),
                ('os_cpu', models.CharField(blank=True, max_length=255, null=True)),
                ('front_cam', models.CharField(blank=True, max_length=255, null=True)),
                ('camera', models.CharField(blank=True, max_length=255, null=True)),
                ('pin', models.CharField(blank=True, max_length=255, null=True)),
                ('screen', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.FileField(null=True, upload_to='images/')),
                ('price', models.BigIntegerField(null=True)),
                ('sale', models.BigIntegerField(null=True)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='variant_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='variant_deleted', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='products.product')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='variant_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'variant',
            },
        ),
    ]
