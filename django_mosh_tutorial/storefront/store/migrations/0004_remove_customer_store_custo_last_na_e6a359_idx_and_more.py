# Generated by Django 5.0 on 2024-01-01 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_customer_store_custo_last_na_e6a359_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='customer',
            name='store_custo_last_na_e6a359_idx',
        ),
        migrations.AlterModelTable(
            name='customer',
            table=None,
        ),
    ]