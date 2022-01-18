# Generated by Django 4.0.1 on 2022-01-18 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world_data', '0005_airwaterquality'),
    ]

    operations = [
        migrations.CreateModel(
            name='Iso',
            fields=[
                ('country', models.CharField(default=None, max_length=200, primary_key=True, serialize=False)),
                ('iso2', models.CharField(blank=True, default=None, max_length=2, null=True)),
                ('iso3', models.CharField(blank=True, default=None, max_length=3, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='airwaterquality',
            name='city',
            field=models.CharField(max_length=200),
        ),
    ]
