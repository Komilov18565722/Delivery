# Generated by Django 4.2 on 2023-05-01 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_orders_delivery_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='delivery_fee',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_weight',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='orders',
            name='period',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.TextField(),
        ),
    ]
