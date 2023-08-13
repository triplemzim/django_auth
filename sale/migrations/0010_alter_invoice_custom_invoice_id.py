# Generated by Django 4.2.3 on 2023-08-13 08:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0009_alter_invoice_custom_invoice_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='custom_invoice_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
