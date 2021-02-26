from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chaines(models.Model):
    id_chaine = models.CharField(max_length=50)
    nom = models.CharField(max_length=100)
    icon = models.CharField(max_length=500, null=True)
    url = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.nom

class Programmes(models.Model):
    titre_informatif = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=3000, null=True)
    date_realisation = models.IntegerField(null=True)
    icon = models.CharField(max_length=500, null=True)
    url = models.CharField(max_length=500, null=True)
    public = models.IntegerField(null=True)
    aide_sourd = models.BooleanField(null=True)
    note = models.SmallIntegerField(null=True)
    critique = models.CharField(max_length=2000, null=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    chaines = models.ForeignKey(
        Chaines, on_delete=models.CASCADE
    )

    # class Meta:
    #     ordering = ['date_debut']

    # def __str__(self):
    #     return self.??????????????

class Titres(models.Model):
    programmes = models.ForeignKey(
        Programmes, on_delete=models.CASCADE
    )
    nom = models.CharField(max_length=150)

    def __str__(self):
        return self.nom

class Realisateur(models.Model):
    programmes = models.ForeignKey(
        Programmes, on_delete=models.CASCADE
    )
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class Scenariste(models.Model):
    programmes = models.ForeignKey(
        Programmes, on_delete=models.CASCADE
    )
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class Acteurs(models.Model):
    programmes = models.ForeignKey(
        Programmes, on_delete=models.CASCADE
    )
    nom = models.CharField(max_length=200)
    role = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nom

class Series(models.Model):
    programmes = models.ForeignKey(
        Programmes, on_delete=models.CASCADE
    )
    serie = models.SmallIntegerField(null=True)
    episode = models.SmallIntegerField(null=True)
    partie = models.SmallIntegerField(null=True)

    # def __str__(self):
    #     return self.???????????

class Categories(models.Model):
    nom = models.CharField(max_length=150)
    programmes = models.ManyToManyField(Programmes)
    def __str__(self):
        return self.nom


class PaysRealisation(models.Model):
    nom = models.CharField(max_length=60)
    programmes = models.ManyToManyField(Programmes)
    def __str__(self):
        return self.nom


class Compositeurs(models.Model):
    programmes = models.ForeignKey(
        Programmes, on_delete=models.CASCADE
    )
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class Recherche(models.Model):
    recherche = models.CharField(max_length=200, null=True, blank=True)
    max_resultats = models.SmallIntegerField()
    programmes = models.ManyToManyField(Programmes)
    chaines = models.ManyToManyField(Chaines)
    date_creation = models.DateTimeField(auto_now=True)
    utilisateur = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.recherche


class RechercheSpecifique(models.Model):
    titre = models.CharField(max_length=150, null=True, blank=True)
    titre_informatif = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    realisateur = models.CharField(max_length=200, null=True, blank=True)
    acteur = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=200, null=True, blank=True)
    scenariste = models.CharField(max_length=200, null=True, blank=True)
    date_realisation = models.SmallIntegerField(null=True, blank=True)
    categories = models.CharField(max_length=150, null=True, blank=True)
    serie = models.SmallIntegerField(null=True, blank=True)
    episode = models.SmallIntegerField(null=True, blank=True)
    partie = models.SmallIntegerField(null=True, blank=True)
    pays_realisation = models.CharField(max_length=200, null=True, blank=True)
    public = models.SmallIntegerField(null=True, blank=True)
    aide_sourd = models.BooleanField(null=True, blank=True)
    note = models.SmallIntegerField(null=True, blank=True)
    critique = models.CharField(max_length=100, null=True, blank=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    recherche = models.ForeignKey(
        Recherche, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.recherche


class BouquetTv(models.Model):
    nom = models.CharField(max_length=100)
    chaines = models.ManyToManyField(Chaines, through='BouquetsChaines')

    def __str__(self):
        return self.nom

class BouquetsChaines(models.Model):
    chaines = models.ForeignKey(Chaines, on_delete=models.CASCADE)
    bouquettv = models.ForeignKey(BouquetTv, on_delete=models.CASCADE)
    numero = models.IntegerField(null=True)
