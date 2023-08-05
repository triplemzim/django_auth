# Generated by Django 4.2.3 on 2023-08-05 15:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Depot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=32)),
                ('code', models.CharField(max_length=32, unique=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Depot',
                'verbose_name_plural': 'Depots',
            },
        ),
    ]