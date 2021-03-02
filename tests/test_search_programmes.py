import datetime
from datetime import timedelta

from pytest import fixture, mark

from django.contrib.auth.models import User
from django.utils.timezone import make_aware

from programmes.management.commands.search_programmes import Command
from programmes.models import (
    Categories,
    PaysRealisation,
    Programmes,
    Chaines,
    Scenariste,
    Series,
    Titres,
    Realisateur,
    Acteurs,
    Recherche,
    RechercheSpecifique,
)


@fixture
def db_feed():
    return Command()


@mark.django_db
def test_search_programmes_with_a_recherche_field(db_feed):

    france_3 = Chaines(id_chaine="france_3", nom="FRANCE 3")
    france_3.save()

    user = User(
        username="Mel",
        first_name="Mell",
        email="mell@gmail.com",
        password="1234simplepassword",
    )
    user.save()

    recherche = Recherche(
        recherche="manon des sources",
        max_resultats=3,
        utilisateur_id=user.id,
        date_creation=make_aware(datetime.datetime.now()),
    )
    recherche.save()
    recherche.chaines.add(france_3.id)

    specific_search = RechercheSpecifique(recherche_id=recherche.id)
    specific_search.save()

    prog = Programmes(
        titre_informatif="Manon des sources",
        chaines_id=france_3.id,
        date_debut=make_aware(datetime.datetime.now() + timedelta(7)),
        date_fin=make_aware(datetime.datetime.now() + timedelta(8)),
    )
    prog.save()

    db_feed.search_progs()

    assert recherche.programmes.all()[0].id == prog.id


@mark.django_db
def test_search_programmes_with_letter_accent_and_case_insensitivity(db_feed):

    france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
    france_3.save()
    id_france_3 = france_3.id

    user = User(
        username="Mel",
        first_name="Mell",
        email="mell@gmail.com",
        password="1234simplepassword",
    )
    user.save()

    recherche = Recherche(
        recherche="mârCel",
        max_resultats=3,
        utilisateur_id=user.id,
        date_creation=make_aware(datetime.datetime.now()),
    )
    recherche.save()
    recherche.chaines.add(france_3.id)

    specific_search = RechercheSpecifique(
        recherche_id=recherche.id,
        titre="la gloîre de mon pere",
        titre_informatif="titre_pagnôl",
        description="Un film de Pagnôl",
        realisateur="robért",
        acteur="JULIÊN",
        role="marcèl",
        scenariste="LOUÎS",
        date_realisation=1990,
        categories="FÏLM",
        serie=1,
        episode=2,
        partie=3,
        pays_realisation="France",
        public=18,
        aide_sourd=True,
        note=5,
        critique="c'est trop bièn",
    )

    specific_search.save()

    gloire = Programmes.objects.create(
        chaines=france_3,
        date_debut=make_aware(datetime.datetime.now() + timedelta(7)),
        date_fin=make_aware(datetime.datetime.now() + timedelta(8)),
        titre_informatif="Titre_pâgnol",
        description="Un film de Pâgnol...",
        date_realisation=1990,
        public=18,
        aide_sourd=True,
        note=5,
        critique="C'est trôp bien",
    )
    gloire.save()

    titre_gloire = Titres.objects.create(
        programmes_id=gloire.id,
        nom="La gloire de mon Père",
    )
    titre_gloire.save()

    realisateur = Realisateur.objects.create(
        programmes_id=gloire.id,
        nom="Yves Rôbert",
    )
    realisateur.save()

    acteur = Acteurs.objects.create(
        programmes_id=gloire.id, nom="Jûlien CIAMACA", role="Mârcel Pagnol"
    )
    acteur.save()

    scenariste = Scenariste.objects.create(
        programmes_id=gloire.id,
        nom="Lôuis Nucera",
    )
    scenariste.save()

    categorie = Categories.objects.create(nom="fîlm")
    categorie.save()
    categorie.programmes.add(gloire.id)

    series = Series.objects.create(
        serie=1, episode=2, partie=3, programmes_id=gloire.id
    )
    series.save()

    pays_realisation = PaysRealisation.objects.create(nom="Frânce")
    pays_realisation.save()
    pays_realisation.programmes.add(gloire.id)

    db_feed.search_progs()

    assert recherche.programmes.all()[0].id == gloire.id
