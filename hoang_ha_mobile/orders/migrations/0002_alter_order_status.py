# Generated by Django 4.0.4 on 2022-07-19 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='Chờ xác nhận', max_length=255),
        ),
    ]