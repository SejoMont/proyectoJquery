# Generated by Django 4.2.1 on 2023-06-01 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0003_alter_viaje_desplazamientoida_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alojamiento',
            old_name='nhuespuedes',
            new_name='nhuespedes',
        ),
    ]
