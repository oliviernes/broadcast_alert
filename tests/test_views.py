"""Test views in broadcast app"""
import datetime

from io import DEFAULT_BUFFER_SIZE

from django.utils.timezone import make_aware
from django.forms import forms
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from unittest.mock import patch
from pytest import mark

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

from urllib.parse import urlencode

import pdb

####################
#   welcome view   #
####################


@mark.django_db
def test_welcome():

    client = Client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.templates[0].name == "programmes/welcome.html"
    assert response.templates[1].name == "programmes/base.html"


####################
#   login view     #
####################


class TestLogin:

    client = Client()

    def test_login(self):

        response = self.client.get("/login/")

        assert response.status_code == 200
        assert response.templates[0].name == "registration/login.html"
        assert response.templates[1].name == "programmes/base.html"

    @mark.django_db
    def test_login_valid_user(self):
        User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

        response_login = self.client.login(
            username="lennon@thebeatles.com", password="johnpassword"
        )

        response_post = self.client.post(
            "/login/",
            {"username": "lennon@thebeatles.com", "password": "johnpassword"},
        )

        assert response_login == True
        assert response_post.url == "/my_account/"
        assert response_post.status_code == 302

    @mark.django_db
    def test_login_wrong_user(self):

        response = self.client.post(
            "/login/", {"username": "tartampion", "password": "johnpassword"}
        )

        assert response.status_code == 200
        assert response.templates[0].name == "registration/login.html"
        assert response.templates[1].name == "programmes/base.html"

    @mark.django_db
    def test_login_wrong_password(self):

        User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

        response_login = self.client.login(
            username="lennon@thebeatles.com", password="wrongpassword"
        )

        response_post = self.client.post(
            "/login/",
            {"username": "lennon@thebeatles.com", "password": "wrongpassword"},
        )

        assert response_login == False
        assert response_post.status_code == 200
        assert response_post.templates[0].name == "registration/login.html"
        assert response_post.templates[1].name == "programmes/base.html"

    @mark.django_db
    def test_login_no_user_recorded(self):

        response = self.client.login(
            username="lennon@thebeatles.com", password="johnpassword"
        )

        assert response == False


####################
#   signup view    #
####################


class TestSignup:

    client = Client()

    def test_signup(self):

        response = self.client.get("/signup/")

        assert response.status_code == 200
        assert response.templates[0].name == "registration/signup.html"
        assert response.templates[1].name == "programmes/base.html"

    @mark.django_db
    def test_signup_right_infos(self):

        response = self.client.post(
            "/signup/",
            {
                "username": "Mell1",
                "first_name": "Mell",
                "last_name": "MAMAMA",
                "email": "mell6@gmail.com",
                "password1": "monsupermdp1234",
                "password2": "monsupermdp1234",
            },
        )

        users = User.objects.all()

        assert response.url == "/my_account/"
        assert response.status_code == 302
        assert users.count() == 1
        assert users[0].username == "Mell1"
        assert users[0].first_name == "Mell"
        assert users[0].last_name == "MAMAMA"
        assert users[0].email == "mell6@gmail.com"

    @mark.django_db
    def test_signup_user_incorrect_data(self):

        response = self.client.post(
            "/signup/",
            {
                "username": "",
                "first_name": "",
                "last_name": "",
                "email": "pimail.com",
                "password1": "aa",
                "password2": "bb",
            },
        )

        users = User.objects.all()

        assert response.status_code == 200
        assert response.templates[0].name == "registration/signup.html"
        assert response.templates[1].name == "programmes/base.html"
        assert users.count() == 0

    @mark.django_db
    def test_signup_user_email_already_used(self):

        User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

        response = self.client.post(
            "/signup/",
            {
                "username": "Mell1",
                "first_name": "Mell",
                "last_name": "MAMAMA",
                "email": "lennon@thebeatles.com",
                "password1": "monsupermdp1234",
                "password2": "monsupermdp1234",
            },
        )

        users = User.objects.all()

        assert response.status_code == 200
        assert response.templates[0].name == "registration/signup.html"
        assert response.templates[1].name == "programmes/base.html"
        assert users.count() == 1


#####################
#   my_account view #
#####################


def test_my_account():

    client = Client()
    response = client.get("/my_account/")

    assert response.status_code == 200
    assert response.templates[0].name == "registration/account.html"
    assert response.templates[1].name == "programmes/base.html"


#################
#   logout view #
#################


def test_logout_view():

    client = Client()
    response = client.get("/logout")

    assert response.status_code == 200
    assert response.templates[0].name == "registration/logged_out.html"
    assert response.templates[1].name == "programmes/base.html"


####################
#   search view    #
####################


class TestSearch:

    client = Client()

    @mark.django_db
    def test_no_results_programmes(self):

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()
        id_france_3 = france_3.id

        data = urlencode(
            {
                "recherche": "La gloire de mon Père",
                "chaines_tv": id_france_3,
                "max_resultats": 4,
                "note": 0,
            }
        )

        response_post = self.client.post(
            reverse("welcome"), data, content_type="application/x-www-form-urlencoded"
        )
        assert response_post.status_code == 200
        assert len(response_post.context["info_programmes"]) == 0
        assert response_post.templates[0].name == "programmes/results.html"

    @mark.django_db
    def test_recherche_give_one_result(self):

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()
        id_france_3 = france_3.id

        gloire = Programmes.objects.create(
            chaines=france_3,
            date_debut=make_aware(datetime.datetime(3021, 2, 19, 17, 10, 41)),
            date_fin=make_aware(datetime.datetime(3022, 2, 19, 17, 10, 41)),
        )
        gloire.save()
        titre_gloire = Titres.objects.create(
            programmes_id=gloire.id,
            nom="La gloire de mon Père",
        )
        titre_gloire.save()

        data = urlencode(
            {
                "recherche": "La gloire de mon Père",
                "chaines_tv": id_france_3,
                "max_resultats": 4,
                "note": 0,
            }
        )

        response_post = self.client.post(
            reverse("welcome"), data, content_type="application/x-www-form-urlencoded"
        )
        assert response_post.status_code == 200
        assert len(response_post.context["info_programmes"]) == 1
        assert (
            response_post.context["info_programmes"][0]["titres"][0].nom
            == "La gloire de mon Père"
        )
        assert response_post.context["info_programmes"][0]["chaine"] == "FRANCE 3"
        assert response_post.templates[0].name == "programmes/results.html"

    @mark.django_db
    def test_recherche_and_recherche_specifique_with_letter_cases_insensitivity(self):

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()
        id_france_3 = france_3.id

        gloire = Programmes.objects.create(
            chaines=france_3,
            date_debut=make_aware(datetime.datetime(3021, 2, 19, 17, 10, 41)),
            date_fin=make_aware(datetime.datetime(3022, 2, 19, 17, 10, 41)),
            titre_informatif="Titre_pagnol",
            description="Un film de Pagnol...",
            date_realisation=1990,
            public=18,
            aide_sourd=True,
            note=5,
            critique="C'est trop bien",
        )
        gloire.save()

        titre_gloire = Titres.objects.create(
            programmes_id=gloire.id,
            nom="La gloire de mon Père",
        )
        titre_gloire.save()

        realisateur = Realisateur.objects.create(
            programmes_id=gloire.id,
            nom="Yves Robert",
        )
        realisateur.save()

        acteur = Acteurs.objects.create(
            programmes_id=gloire.id, nom="Julien CIAMACA", role="Marcel Pagnol"
        )
        acteur.save()

        scenariste = Scenariste.objects.create(
            programmes_id=gloire.id,
            nom="Louis Nucera",
        )
        scenariste.save()

        categorie = Categories.objects.create(nom="film")
        categorie.save()
        categorie.programmes.add(gloire.id)

        series = Series.objects.create(
            serie=1, episode=2, partie=3, programmes_id=gloire.id
        )
        series.save()

        pays_realisation = PaysRealisation.objects.create(nom="France")
        pays_realisation.save()
        pays_realisation.programmes.add(gloire.id)

        data = urlencode(
            {
                "chaines_tv": id_france_3,
                "recherche": "marcel",
                "max_resultats": 4,
                "titre": "la gloire de mon père",
                "titre_informatif": "titre_pagnol",
                "description": "Un film de Pagnol",
                "realisateur": "robert",
                "acteur": "JULIEN",
                "role": "marcel",
                "scenariste": "LOUIS",
                "date_realisation": 1990,
                "categories": "FILM",
                "serie": 1,
                "episode": 2,
                "partie": 3,
                "pays_realisation": "France",
                "public": 18,
                "aide_sourd": True,
                "note": 5,
                "critique": "c'est trop bien",
            }
        )

        response_post = self.client.post(
            reverse("welcome"), data, content_type="application/x-www-form-urlencoded"
        )
        assert response_post.status_code == 200
        assert len(response_post.context["info_programmes"]) == 1
        assert (
            response_post.context["info_programmes"][0]["titres"][0].nom
            == "La gloire de mon Père"
        )
        assert response_post.context["info_programmes"][0]["chaine"] == "FRANCE 3"
        assert (
            response_post.context["info_programmes"][0]["programme"].titre_informatif
            == "Titre_pagnol"
        )
        assert (
            response_post.context["info_programmes"][0]["programme"].description
            == "Un film de Pagnol..."
        )
        assert (
            response_post.context["info_programmes"][0]["realisateur"][0].nom
            == "Yves Robert"
        )
        assert (
            response_post.context["info_programmes"][0]["acteurs"][0].nom
            == "Julien CIAMACA"
        )
        assert (
            response_post.context["info_programmes"][0]["acteurs"][0].role
            == "Marcel Pagnol"
        )
        assert (
            response_post.context["info_programmes"][0]["scenariste"][0].nom
            == "Louis Nucera"
        )
        assert (
            response_post.context["info_programmes"][0]["programme"].date_realisation
            == 1990
        )
        assert (
            response_post.context["info_programmes"][0]["categories"][0].nom == "film"
        )
        assert response_post.context["info_programmes"][0]["series"][0].serie == 1
        assert response_post.context["info_programmes"][0]["series"][0].episode == 2
        assert response_post.context["info_programmes"][0]["series"][0].partie == 3
        assert response_post.context["info_programmes"][0]["pays"][0].nom == "France"
        assert (
            response_post.context["info_programmes"][0]["programme"].aide_sourd == True
        )
        assert response_post.context["info_programmes"][0]["programme"].note == 5
        assert (
            response_post.context["info_programmes"][0]["programme"].critique
            == "C'est trop bien"
        )
        assert response_post.templates[0].name == "programmes/results.html"

    @mark.django_db
    def test_recherche_and_recherche_specifique_with_letter_accent_insensitivity(self):

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()
        id_france_3 = france_3.id

        gloire = Programmes.objects.create(
            chaines=france_3,
            date_debut=make_aware(datetime.datetime(3021, 2, 19, 17, 10, 41)),
            date_fin=make_aware(datetime.datetime(3022, 2, 19, 17, 10, 41)),
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

        data = urlencode(
            {
                "chaines_tv": id_france_3,
                "recherche": "marcel",
                "max_resultats": 4,
                "titre": "la gloîre de mon pere",
                "titre_informatif": "titre_pagnôl",
                "description": "Un film de Pagnôl",
                "realisateur": "robért",
                "acteur": "JULIÊN",
                "role": "marcèl",
                "scenariste": "LOUÎS",
                "date_realisation": 1990,
                "categories": "FÏLM",
                "serie": 1,
                "episode": 2,
                "partie": 3,
                "pays_realisation": "France",
                "public": 18,
                "aide_sourd": True,
                "note": 5,
                "critique": "c'est trop bièn",
            }
        )

        response_post = self.client.post(
            reverse("welcome"), data, content_type="application/x-www-form-urlencoded"
        )
        assert response_post.status_code == 200
        assert len(response_post.context["info_programmes"]) == 1
        assert (
            response_post.context["info_programmes"][0]["titres"][0].nom
            == "La gloire de mon Père"
        )
        assert response_post.context["info_programmes"][0]["chaine"] == "FRANCE 3"
        assert (
            response_post.context["info_programmes"][0]["programme"].titre_informatif
            == "Titre_pâgnol"
        )
        assert (
            response_post.context["info_programmes"][0]["programme"].description
            == "Un film de Pâgnol..."
        )
        assert (
            response_post.context["info_programmes"][0]["realisateur"][0].nom
            == "Yves Rôbert"
        )
        assert (
            response_post.context["info_programmes"][0]["acteurs"][0].nom
            == "Jûlien CIAMACA"
        )
        assert (
            response_post.context["info_programmes"][0]["acteurs"][0].role
            == "Mârcel Pagnol"
        )
        assert (
            response_post.context["info_programmes"][0]["scenariste"][0].nom
            == "Lôuis Nucera"
        )
        assert (
            response_post.context["info_programmes"][0]["programme"].date_realisation
            == 1990
        )
        assert (
            response_post.context["info_programmes"][0]["categories"][0].nom == "fîlm"
        )
        assert response_post.context["info_programmes"][0]["series"][0].serie == 1
        assert response_post.context["info_programmes"][0]["series"][0].episode == 2
        assert response_post.context["info_programmes"][0]["series"][0].partie == 3
        assert response_post.context["info_programmes"][0]["pays"][0].nom == "Frânce"
        assert (
            response_post.context["info_programmes"][0]["programme"].aide_sourd == True
        )
        assert response_post.context["info_programmes"][0]["programme"].note == 5
        assert (
            response_post.context["info_programmes"][0]["programme"].critique
            == "C'est trôp bien"
        )
        assert response_post.templates[0].name == "programmes/results.html"

    @mark.django_db
    def test_no_recherche_by_user(self):

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()
        id_france_3 = france_3.id

        data = urlencode({"chaines_tv": id_france_3, "max_resultats": 4, "note": 0})

        response_post = self.client.post(
            reverse("welcome"), data, content_type="application/x-www-form-urlencoded"
        )
        assert response_post.status_code == 200
        assert len(response_post.context["info_programmes"]) == 0
        assert response_post.templates[0].name == "programmes/results.html"

    @mark.django_db
    def test_get_welcome_page(self):

        response_get = self.client.get(reverse("welcome"))

        assert response_get.status_code == 200
        assert response_get.templates[0].name == "programmes/welcome.html"

    @mark.django_db
    def test_bouquet_is_valid(self):

        data = urlencode({"bouquets": 2})

        response_post = self.client.post(
            reverse("welcome"), data, content_type="application/x-www-form-urlencoded"
        )

        assert response_post.status_code == 200
        assert response_post.templates[0].name == "programmes/welcome.html"

    @mark.django_db
    def test_bouquet_all_channels(self):

        data = urlencode({"bouquets": 6})

        response_post = self.client.post(
            reverse("welcome"), data, content_type="application/x-www-form-urlencoded"
        )

        assert response_post.status_code == 200
        assert response_post.templates[0].name == "programmes/welcome.html"

    @mark.django_db
    def test_bouquet_is_not_valid(self):

        data = urlencode({"bouquets": 7})

        response_post = self.client.post(
            reverse("welcome"), data, content_type="application/x-www-form-urlencoded"
        )

        assert response_post.status_code == 200
        assert response_post.templates[0].name == "programmes/welcome.html"

    @mark.django_db
    def test_save_search_with_user_not_connected(self):

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()
        id_france_3 = france_3.id

        data = urlencode(
            {
                "chaines_tv": id_france_3,
                "recherche": "Marcel",
                "max_resultats": 4,
                "my_search": ["Enregistrer la recherche"],
            }
        )

        response_post = self.client.post(
            reverse("welcome"), data, content_type="application/x-www-form-urlencoded"
        )
        assert response_post.status_code == 302

    @mark.django_db
    def test_save_search(self):

        User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

        self.client.login(username="lennon@thebeatles.com", password="johnpassword")

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()
        id_france_3 = france_3.id

        data = urlencode(
            {
                "chaines_tv": id_france_3,
                "recherche": "Marcel",
                "max_resultats": 4,
                "titre": "La gloire de mon Père",
                "note": 5,
                "my_search": ["Enregistrer la recherche"],
            }
        )

        response_post = self.client.post(
            reverse("welcome"), data, content_type="application/x-www-form-urlencoded"
        )
        assert response_post.status_code == 200
        assert response_post.templates[0].name == "programmes/registered_info.html"

    @mark.django_db
    def test_saving_with_all_None_search_fields(self):

        User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

        self.client.login(username="lennon@thebeatles.com", password="johnpassword")

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()
        id_france_3 = france_3.id

        data = urlencode(
            {
                "chaines_tv": id_france_3,
                "max_resultats": 4,
                "my_search": ["Enregistrer la recherche"],
                "note": 0,
            }
        )

        response_post = self.client.post(
            reverse("welcome"), data, content_type="application/x-www-form-urlencoded"
        )
        assert response_post.status_code == 200
        assert response_post.templates[0].name == "programmes/no_search.html"


######################
#   my_search view   #
######################


class TestMySearch:

    client = Client()

    @mark.django_db
    def test_display_registered_search(self):

        User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

        self.client.login(username="lennon@thebeatles.com", password="johnpassword")

        response_get = self.client.get(reverse("my_search"))

        assert response_get.status_code == 200
        assert response_get.templates[0].name == "programmes/my_search.html"

    @mark.django_db
    def test_display_registered_search_info_without_recherche_specifique(self):

        user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

        self.client.login(username="lennon@thebeatles.com", password="johnpassword")

        recherche = Recherche(
            recherche="gloire de mon père", max_resultats=3, utilisateur_id=user.id
        )

        recherche.save()

        response_get = self.client.get(reverse("my_search"))

        assert response_get.status_code == 200
        assert response_get.templates[0].name == "programmes/my_search.html"

    @mark.django_db
    def test_display_registered_search_info_with_recherche_specifique(self):

        user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

        self.client.login(username="lennon@thebeatles.com", password="johnpassword")

        recherche = Recherche(
            recherche="gloire de mon père", max_resultats=3, utilisateur_id=user.id
        )

        recherche.save()

        recherche_specifique = RechercheSpecifique(
            titre="La gloire de mon père",
            description="un film...",
            recherche_id=recherche.id,
        )

        recherche_specifique.save()

        response_get = self.client.get(reverse("my_search"))

        assert response_get.status_code == 200
        assert response_get.templates[0].name == "programmes/my_search.html"


######################
#   delete view      #
######################


class TestDelete:

    client = Client()

    @mark.django_db
    def test_delete_a_registered_search_with_connected_user(self):

        user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

        self.client.login(username="lennon@thebeatles.com", password="johnpassword")

        recherche = Recherche(
            recherche="gloire de mon père", max_resultats=3, utilisateur_id=user.id
        )

        recherche.save()

        recherche_specifique = RechercheSpecifique(
            titre="La gloire de mon père",
            description="un film...",
            recherche_id=recherche.id,
        )

        recherche_specifique.save()

        assert len(Recherche.objects.all()) == 1

        response_post = self.client.post(reverse("delete", kwargs={"pk": recherche.id}))

        assert response_post.status_code == 200
        assert len(Recherche.objects.all()) == 0
        assert response_post.templates[0].name == "programmes/welcome.html"

    @mark.django_db
    def test_delete_a_registered_search_with_user_not_connected(self):

        user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

        recherche = Recherche(
            recherche="gloire de mon père", max_resultats=3, utilisateur_id=user.id
        )

        recherche.save()

        recherche_specifique = RechercheSpecifique(
            titre="La gloire de mon père",
            description="un film...",
            recherche_id=recherche.id,
        )

        recherche_specifique.save()

        assert len(Recherche.objects.all()) == 1

        response_post = self.client.post(reverse("delete", kwargs={"pk": recherche.id}))

        assert response_post.status_code == 200
        assert len(Recherche.objects.all()) == 1
        assert response_post.templates[0].name == "programmes/auth_info.html"

    @mark.django_db
    def test_try_delete_a_registered_search_of_an_other_user(self):

        User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
        user_mell = User.objects.create_user(
            "mell", "mell@thebeatles.com", "mellpassword"
        )

        recherche = Recherche(
            recherche="gloire de mon père", max_resultats=3, utilisateur_id=user_mell.id
        )

        recherche.save()

        recherche_specifique = RechercheSpecifique(
            titre="La gloire de mon père",
            description="un film...",
            recherche_id=recherche.id,
        )

        recherche_specifique.save()

        self.client.login(username="lennon@thebeatles.com", password="johnpassword")

        assert len(Recherche.objects.all()) == 1

        response_post = self.client.post(reverse("delete", kwargs={"pk": recherche.id}))

        assert response_post.status_code == 200
        assert len(Recherche.objects.all()) == 1
        assert response_post.templates[0].name == "programmes/not_delete.html"


######################
#   my_results view  #
######################


class TestMyResults:

    client = Client()

    @mark.django_db
    def test_display_my_search_results_with_no_results(self):

        user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

        self.client.login(username="lennon@thebeatles.com", password="johnpassword")

        recherche = Recherche(
            recherche="gloire de mon père", max_resultats=3, utilisateur_id=user.id
        )

        recherche.save()

        recherche_specifique = RechercheSpecifique(
            titre="La gloire de mon père",
            description="un film...",
            recherche_id=recherche.id,
        )

        recherche_specifique.save()

        response_get = self.client.get(
            reverse("my_results", kwargs={"my_search_id": recherche.id})
        )

        assert response_get.context["info_search"]["recherche"] == "gloire de mon père"
        assert response_get.context["info_search"]["titre"] == "La gloire de mon père"
        assert len(response_get.context["info_programmes"]) == 0
        assert response_get.status_code == 200
        assert response_get.templates[0].name == "programmes/results.html"

    @mark.django_db
    def test_display_my_search_results_with_one_results(self):

        user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

        self.client.login(username="lennon@thebeatles.com", password="johnpassword")

        recherche = Recherche(
            recherche="gloire de mon père", max_resultats=3, utilisateur_id=user.id
        )

        recherche.save()

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()

        recherche.chaines.add(france_3.id)

        recherche_specifique = RechercheSpecifique(
            titre="La gloire de mon père",
            description="un film de",
            recherche_id=recherche.id,
        )

        recherche_specifique.save()

        gloire = Programmes.objects.create(
            chaines=france_3,
            date_debut=make_aware(datetime.datetime(3021, 2, 19, 17, 10, 41)),
            date_fin=make_aware(datetime.datetime(3022, 2, 19, 17, 10, 41)),
            titre_informatif="Titre_pagnol",
            description="Un film de Pagnol...",
            date_realisation=1990,
            public=18,
            aide_sourd=True,
            note=5,
            critique="C'est trop bien",
        )
        gloire.save()

        titre_gloire = Titres.objects.create(
            programmes_id=gloire.id,
            nom="La gloire de mon Père",
        )
        titre_gloire.save()

        response_get = self.client.get(
            reverse("my_results", kwargs={"my_search_id": recherche.id})
        )

        assert response_get.context["info_search"]["recherche"] == "gloire de mon père"
        assert response_get.context["info_search"]["titre"] == "La gloire de mon père"
        assert len(response_get.context["info_programmes"]) == 1
        assert (
            response_get.context["info_programmes"][0]["titres"][0].nom
            == "La gloire de mon Père"
        )
        assert (
            response_get.context["info_programmes"][0]["programme"].description
            == "Un film de Pagnol..."
        )
        assert response_get.status_code == 200
        assert response_get.templates[0].name == "programmes/results.html"

    @mark.django_db
    def test_cannot_display_my_search_results_of_an_other_user(self):

        User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
        user_mell = User.objects.create_user(
            "mell", "mell@thebeatles.com", "mellpassword"
        )

        recherche = Recherche(
            recherche="gloire de mon père", max_resultats=3, utilisateur_id=user_mell.id
        )

        recherche.save()

        recherche_specifique = RechercheSpecifique(
            titre="La gloire de mon père",
            description="un film...",
            recherche_id=recherche.id,
        )

        recherche_specifique.save()

        self.client.login(username="lennon@thebeatles.com", password="johnpassword")

        response_get = self.client.get(
            reverse("my_results", kwargs={"my_search_id": recherche.id})
        )

        assert response_get.status_code == 200
        assert response_get.templates[0].name == "programmes/no_results.html"

    @mark.django_db
    def test_cannot_display_my_search_results_of_an_user_not_connected(self):

        user_mell = User.objects.create_user(
            "mell", "mell@thebeatles.com", "mellpassword"
        )

        recherche = Recherche(
            recherche="gloire de mon père", max_resultats=3, utilisateur_id=user_mell.id
        )

        recherche.save()

        recherche_specifique = RechercheSpecifique(
            titre="La gloire de mon père",
            description="un film...",
            recherche_id=recherche.id,
        )

        recherche_specifique.save()

        response_get = self.client.get(
            reverse("my_results", kwargs={"my_search_id": recherche.id})
        )

        assert response_get.status_code == 200
        assert response_get.templates[0].name == "programmes/auth_info.html"
