# Generated by Django 4.0.4 on 2022-07-25 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='updated_by',
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=10),
        ),
    ]
