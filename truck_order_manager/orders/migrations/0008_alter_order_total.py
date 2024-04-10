# Generated by Django 5.0.4 on 2024-04-09 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_remove_order_created_at_order_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]