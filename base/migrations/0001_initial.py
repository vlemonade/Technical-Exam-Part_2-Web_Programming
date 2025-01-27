# Generated by Django 5.1.2 on 2024-11-05 07:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order_type', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], default='BUY', max_length=4)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.stock')),
            ],
        ),
    ]
