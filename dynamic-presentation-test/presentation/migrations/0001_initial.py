# Generated by Django 5.0.2 on 2024-02-29 17:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
                ('presenter_name', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('present_date', models.CharField(default='زمستان ۱۴۰۱', max_length=255)),
                ('background_image', models.ImageField(upload_to='background_image')),
                ('slug', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(null=True)),
                ('order', models.IntegerField(default=0)),
                ('url', models.CharField(max_length=255)),
                ('presentation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slides', to='presentation.presentation')),
            ],
        ),
    ]
