# Generated by Django 3.1.5 on 2021-01-31 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programmes', '0002_auto_20210130_1700'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chaines',
            old_name='id_chaines',
            new_name='id_chaine',
        ),
    ]