# Generated by Django 4.1 on 2022-08-31 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0006_product_product_image_delete_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, default='mdb-favicon.ico', null=True, upload_to='images/'),
        ),
    ]
