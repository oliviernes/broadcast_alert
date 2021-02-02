# Generated by Django 3.1.5 on 2021-02-02 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programmes', '0003_auto_20210131_0812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bouquettv',
            name='numero',
        ),
        migrations.CreateModel(
            name='BouquetsChaines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(null=True)),
                ('bouquettv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programmes.bouquettv')),
                ('chaines', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programmes.chaines')),
            ],
        ),
        migrations.RemoveField(
            model_name='bouquettv',
            name='chaines',
        ),
        migrations.AddField(
            model_name='bouquettv',
            name='chaines',
            field=models.ManyToManyField(through='programmes.BouquetsChaines', to='programmes.Chaines'),
        ),

    ]
