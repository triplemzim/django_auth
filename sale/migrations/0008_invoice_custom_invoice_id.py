# Generated by Django 4.2.3 on 2023-08-13 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0007_invoice_alter_balance_amount_alter_customer_depot_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='custom_invoice_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]