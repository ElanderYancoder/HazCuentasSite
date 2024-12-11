# Generated by Django 5.1.3 on 2024-11-30 09:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0024_comentario'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='blogpost',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='main_app.categoriablog'),
        ),
    ]
