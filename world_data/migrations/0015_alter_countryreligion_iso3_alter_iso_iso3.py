# Generated by Django 4.0.1 on 2022-01-20 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world_data', '0014_alter_countryreligion_iso3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countryreligion',
            name='iso3',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='iso',
            name='iso3',
            field=models.CharField(blank=True, default=None, max_length=3, null=True, unique=True),
        ),
    ]
