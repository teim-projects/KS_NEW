# Generated by Django 5.0 on 2025-06-13 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kushalapp', '0006_remove_quotation_actual_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='actual_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='gst_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
