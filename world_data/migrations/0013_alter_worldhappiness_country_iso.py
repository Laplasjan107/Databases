# Generated by Django 4.0.1 on 2022-01-20 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world_data', '0012_remove_worldhappiness_country_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worldhappiness',
            name='country_iso',
            field=models.CharField(max_length=3),
        ),
    ]
