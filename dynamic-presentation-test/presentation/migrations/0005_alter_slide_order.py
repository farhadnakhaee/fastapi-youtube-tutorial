# Generated by Django 5.0.2 on 2024-02-29 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0004_alter_slide_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='order',
            field=models.PositiveIntegerField(default=0, max_length=255),
        ),
    ]
