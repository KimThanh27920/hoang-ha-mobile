<<<<<<< HEAD
# Generated by Django 4.0.4 on 2022-07-25 03:20
=======
# Generated by Django 4.0.4 on 2022-07-25 03:09
>>>>>>> b1016d3323a636ead81eab571b52925a8b7bc20c

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='insurance',
            field=models.IntegerField(default=0),
        ),
    ]
