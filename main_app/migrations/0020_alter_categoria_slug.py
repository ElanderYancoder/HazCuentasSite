# Generated by Django 5.1.3 on 2024-11-27 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0019_categoria_faq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]