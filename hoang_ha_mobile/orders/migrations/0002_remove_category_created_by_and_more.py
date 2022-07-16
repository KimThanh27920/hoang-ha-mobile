# Generated by Django 4.0.4 on 2022-07-15 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='category',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='category',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='product',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='product',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='product',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='product',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Variant',
        ),
    ]
