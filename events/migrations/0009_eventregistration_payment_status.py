# Generated by Django 5.1.7 on 2025-03-26 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_eventregistration'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventregistration',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
    ]
