# Generated by Django 4.0.1 on 2022-01-19 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world_data', '0007_iso_numeric'),
    ]

    operations = [
        migrations.AddField(
            model_name='iso',
            name='iso2_continent',
            field=models.CharField(max_length=2, null=True),
        ),
    ]