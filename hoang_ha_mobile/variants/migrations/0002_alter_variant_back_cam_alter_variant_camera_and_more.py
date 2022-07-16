# Generated by Django 4.0.4 on 2022-07-15 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('variants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='back_cam',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='camera',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='color',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='front_cam',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='general',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='network',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='os_cpu',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='pin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='screen',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='size',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='storage',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='strap',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='utilities',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='version',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
