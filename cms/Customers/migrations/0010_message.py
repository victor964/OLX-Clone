# Generated by Django 4.1 on 2022-09-01 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0009_customer_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customers.customer')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customers.buyer')),
            ],
        ),
    ]