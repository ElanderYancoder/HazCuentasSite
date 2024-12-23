# Generated by Django 5.1.3 on 2024-11-16 05:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_notificacion_titulo_alter_notificacion_mensaje'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='noticia',
            name='autor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='noticia',
            name='destacado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='noticia',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes_noticias/'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='fecha_publicacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
