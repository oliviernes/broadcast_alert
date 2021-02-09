import json
import datetime
import pytz

from pytest import fixture, mark

from programmes.management.commands.populate_programmes import Command
from programmes.models import Chaines, Programmes, Titres, Acteurs

@fixture
def db_feed():
    return Command()


@mark.django_db
def test_populate_channels_insertion(db_feed):

    db_feed.populate("teleloisirs_test_populate.json")

    chaine = Chaines.objects.all()[0]
    chaine_last = Chaines.objects.all()[5]

    assert chaine.id == 1
    assert chaine.id_chaine == "187.api-tel.programme-tv.net"
    assert chaine.nom == "TIPIK"
    assert chaine.icon == "https://tel.img.pmdstatic.net/fit/https.3A.2F.2Fprd2-tel-epg-img.2Es3-eu-west-1.2Eamazonaws.2Ecom.2Fchannel.2F8107d72a6d5971bf.2Epng/500x500/_/image.png"
    assert chaine.url == "https://www.programme-tv.net/programme/chaine/programme-tipik-143.html"

    assert chaine_last.id == 6
    assert chaine_last.id_chaine == "1785.api-tel.programme-tv.net"
    assert chaine_last.nom == "GOSPEL MUSIC TV"
    assert chaine_last.icon == "https://tel.img.pmdstatic.net/fit/https.3A.2F.2Fprd2-tel-epg-img.2Es3-eu-west-1.2Eamazonaws.2Ecom.2Fchannel.2F8d58cd3ce94e9ae8.2Epng/500x500/_/image.png"
    assert chaine_last.url == "https://www.programme-tv.net/programme/chaine/programme-gospel-music-tv-346.html"



@mark.django_db
def test_populate_programmes_insertion(db_feed):

    db_feed.populate("teleloisirs_test_populate.json")

    prog = Programmes.objects.all()[0]
    titre = Titres.objects.all()[0]
    prog_piege = Programmes.objects.get(titre_informatif="Piégés")
    # actor = Acteurs.objects.filter(programmes_id=2).order_by('id')
    actor = Acteurs.objects.filter(programmes_id=prog_piege.id).order_by('id')

    print(actor)
    print(actor[0].nom)
    print(prog_piege.categories_set.all())

    chaine_boomerang = Chaines.objects.get(id_chaine="321.api-tel.programme-tv.net")
    
    """Test if the Teleloisirs API return number instead of string for 'sub-title', 'desc', 'icon',
    'url', 'review' fields"""
    prog_9999999 = Programmes.objects.filter(date_debut=datetime.datetime(2021, 2, 5, 11, 25, tzinfo=pytz.UTC),
                                        date_fin=datetime.datetime(2021, 2, 5, 11, 35, tzinfo=pytz.UTC),
                                        chaines=chaine_boomerang.id)
    """Test if a time with 60mn displayed by the API can be registered in the db to 59mn"""
    prog_60 = Programmes.objects.filter(date_debut=datetime.datetime(2021, 2, 5, 11, 59, tzinfo=pytz.UTC),
                                        date_fin=datetime.datetime(2021, 2, 5, 12, 59, tzinfo=pytz.UTC),
                                        chaines=chaine_boomerang.id)

    assert prog.titre_informatif == None
    assert prog.description[:35] == "Vews propose des vidéos d'actualité"
    assert prog.date_realisation == None
    assert prog.icon == "https://tel.img.pmdstatic.net/fit/https.3A.2F.2Fprd2-tel-epg-img.2Es3-eu-west-1.2Eamazonaws.2Ecom.2Fprogram.2Ffc2991d58d90eebd.2Ejpg/1280x720/_/image.jpg"
    assert prog.date_debut == datetime.datetime(2021, 2, 5, 22, 59, tzinfo=pytz.UTC)
    assert prog.date_fin == datetime.datetime(2021, 2, 5, 23, 6, tzinfo=pytz.UTC)
    assert prog.compositeurs_set.all()[0].nom == "cristal distorsion"

    # assert prog_piege.id == 2
    assert prog_piege.date_realisation == 2007
    assert prog_piege.url == "https://www.programme-tv.net/programme/series-tv/r1798-les-4400/854652-pieges/"
    assert prog_piege.public == 10
    assert prog_piege.aide_sourd == False
    assert prog_piege.note == 1
    assert prog_piege.critique == "Un huis clos très tendu pour nos héros."
    assert titre.nom == "Vews"
    assert actor[0].nom =="Bill Campbell"
    assert actor[1].nom =="Patrick Flueger"
    assert actor[7].nom =="Carly Pope"
    assert actor[0].role =="Jordan Collier"
    assert prog_piege.realisateur_set.all()[0].nom == "Tony Westman"
    assert prog_piege.scenariste_set.all()[0].nom == "Adam Levy"
    assert prog_piege.paysrealisation_set.all()[0].nom == "Etats-Unis"
    assert prog_piege.compositeurs_set.all().exists() == False
    assert prog_piege.categories_set.all().order_by('id')[0].nom == "Série"
    assert prog_piege.series_set.all()[0].serie == 3
    assert prog_piege.series_set.all()[0].episode == 7
    assert prog_piege.series_set.all()[0].partie == 0
    assert len(prog_9999999) == 1
    assert len(prog_60) == 1
