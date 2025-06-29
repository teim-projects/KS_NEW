# Generated by Django 5.0 on 2025-06-19 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kushalapp', '0012_alter_lead_assigned_to_operations'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='customer_visited',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='file_upload',
            field=models.FileField(blank=True, null=True, upload_to='lead_files/'),
        ),
        migrations.AddField(
            model_name='lead',
            name='first_call_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='inspection_done',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='lead_type',
            field=models.CharField(blank=True, choices=[('Hot', 'Hot'), ('Warm', 'Warm'), ('Cold', 'Cold'), ('Not Interested', 'Not Interested'), ('Irrelevant', 'Irrelevant')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='quotation_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='quotation_given',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True),
        ),
    ]
