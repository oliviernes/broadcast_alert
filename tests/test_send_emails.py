import datetime
from datetime import timedelta

from pytest import fixture, mark

from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from django.core import mail

from programmes.management.commands.send_emails import Command
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
def test_send_email_one_programme_match_to_a_user(db_feed):

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
        date_creation=make_aware(datetime.datetime.now() - timedelta(1)),
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

    titre_prog = Titres.objects.create(
        programmes_id=prog.id,
        nom="La Manon",
    )
    titre_prog.save()


    recherche.programmes.add(prog.id)

    db_feed.send_email()

    assert mail.outbox[0].subject == "Un programme correspond à votre recherche!"