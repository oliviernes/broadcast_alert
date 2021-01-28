# Generated by Django 3.1.5 on 2021-01-28 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chaines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_chaines', models.CharField(max_length=50)),
                ('nom', models.CharField(max_length=100)),
                ('icon', models.CharField(max_length=500, null=True)),
                ('url', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Programmes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre_informatif', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(max_length=3000, null=True)),
                ('date_realisation', models.IntegerField(null=True)),
                ('icon', models.CharField(max_length=500, null=True)),
                ('url', models.CharField(max_length=500, null=True)),
                ('public', models.IntegerField(null=True)),
                ('aide_sourd', models.BooleanField(null=True)),
                ('note', models.IntegerField(null=True)),
                ('critique', models.CharField(max_length=2000, null=True)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('chaines', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programmes.chaines')),
            ],
        ),
        migrations.CreateModel(
            name='Recherche',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recherche', models.CharField(max_length=200, null=True)),
                ('match_all', models.BooleanField()),
                ('max_resultats', models.IntegerField()),
                ('chaines', models.ManyToManyField(to='programmes.Chaines')),
                ('programmes', models.ManyToManyField(to='programmes.Programmes')),
            ],
        ),
        migrations.CreateModel(
            name='Titres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('programmes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programmes.programmes')),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serie', models.IntegerField(null=True)),
                ('episode', models.IntegerField(null=True)),
                ('partie', models.IntegerField(null=True)),
                ('programmes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programmes.programmes')),
            ],
        ),
        migrations.CreateModel(
            name='Scenariste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('programmes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programmes.programmes')),
            ],
        ),
        migrations.CreateModel(
            name='RechercheSpecifique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=150, null=True)),
                ('titre_informatif', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('realisateur', models.CharField(max_length=200, null=True)),
                ('acteur', models.CharField(max_length=200, null=True)),
                ('role', models.CharField(max_length=200, null=True)),
                ('scenariste', models.CharField(max_length=200, null=True)),
                ('date_realisation', models.IntegerField(null=True)),
                ('categories', models.CharField(max_length=150, null=True)),
                ('serie', models.IntegerField(null=True)),
                ('episode', models.IntegerField(null=True)),
                ('partie', models.IntegerField(null=True)),
                ('pays_realisation', models.CharField(max_length=200, null=True)),
                ('public', models.IntegerField(null=True)),
                ('aide_sourd', models.BooleanField(null=True)),
                ('note', models.IntegerField(null=True)),
                ('critique', models.CharField(max_length=100, null=True)),
                ('date_debut', models.DateField(null=True)),
                ('date_fin', models.DateField(null=True)),
                ('recherche', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programmes.recherche')),
            ],
        ),
        migrations.CreateModel(
            name='Realisateur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('programmes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programmes.programmes')),
            ],
        ),
        migrations.CreateModel(
            name='PaysRealisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=60)),
                ('programmes', models.ManyToManyField(to='programmes.Programmes')),
            ],
        ),
        migrations.CreateModel(
            name='Compositeurs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('programmes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programmes.programmes')),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('programmes', models.ManyToManyField(to='programmes.Programmes')),
            ],
        ),
        migrations.CreateModel(
            name='BouquetTv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
                ('chaines', models.ManyToManyField(to='programmes.Chaines')),
            ],
        ),
        migrations.CreateModel(
            name='Acteurs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=200, null=True)),
                ('programmes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programmes.programmes')),
            ],
        ),
    ]