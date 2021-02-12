# Generated by Django 3.1.5 on 2021-02-09 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programmes', '0004_auto_20210202_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programmes',
            name='note',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='recherche',
            name='max_resultats',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='recherchespecifique',
            name='date_realisation',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='recherchespecifique',
            name='episode',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='recherchespecifique',
            name='note',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='recherchespecifique',
            name='partie',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='recherchespecifique',
            name='public',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='recherchespecifique',
            name='serie',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='episode',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='partie',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='serie',
            field=models.SmallIntegerField(null=True),
        ),
    ]