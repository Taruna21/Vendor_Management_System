# Generated by Django 4.2.7 on 2023-12-19 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendors', '0004_alter_purchaseorder_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorder',
            name='quality_rating',
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='acknowledgment_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendorperformance',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='vendorperformance',
            name='fulfillment_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='vendorperformance',
            name='on_time_delivery_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='vendorperformance',
            name='quality_rating',
            field=models.FloatField(default=0),
        ),
    ]
