# Generated by Django 4.0.1 on 2022-01-20 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world_data', '0010_alter_airwaterquality_air_quality_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='worldhappiness',
            name='country_iso',
            field=models.CharField(blank=True, default=None, max_length=3, null=True),
        ),
    ]
