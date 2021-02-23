"""Test views in broadcast app"""
import datetime
from io import DEFAULT_BUFFER_SIZE

from django.utils.timezone import make_aware
from django.forms import forms
from django.test import TestCase, Client
from django.urls import reverse

from unittest.mock import patch
from pytest import mark

from programmes.models import Categories, PaysRealisation, Programmes, Chaines, Scenariste, Series, Titres, Realisateur, Acteurs

from urllib.parse import urlencode

import pdb

class TestResult:

    client = Client()

    @mark.django_db
    def test_no_results_programmes(self):

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()
        id_france_3 = france_3.id

        data = urlencode({'recherche': 'La gloire de mon Père', 'chaines_tv': id_france_3, 'max_resultats': 4})

        response_post = self.client.post(reverse('results'), data, content_type="application/x-www-form-urlencoded")
        assert response_post.status_code == 200
        assert len(response_post.context["info_programmes"]) == 0
        assert response_post.templates[0].name == "programmes/results.html"

    @mark.django_db
    def test_recherche_give_one_result(self):

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()
        id_france_3 = france_3.id

        gloire = Programmes.objects.create(chaines=france_3,
            date_debut=make_aware(datetime.datetime(3021, 2, 19, 17, 10, 41)),
            date_fin=make_aware(datetime.datetime(3022, 2, 19, 17, 10, 41))
        )
        gloire.save()
        titre_gloire = Titres.objects.create(programmes_id=gloire.id,
            nom='La gloire de mon Père',
            )
        titre_gloire.save()

        data = urlencode({'recherche': 'La gloire de mon Père', 'chaines_tv': id_france_3, 'max_resultats': 4})

        response_post = self.client.post(reverse('results'), data, content_type="application/x-www-form-urlencoded")
        assert response_post.status_code == 200
        assert len(response_post.context["info_programmes"]) == 1
        assert response_post.context['info_programmes'][0]['titres'][0].nom == 'La gloire de mon Père'
        assert response_post.context['info_programmes'][0]['chaine'] == 'FRANCE 3'
        assert response_post.templates[0].name == "programmes/results.html"

    @mark.django_db
    def test_recherche_and_recherche_specifique(self):

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()
        id_france_3 = france_3.id

        gloire = Programmes.objects.create(chaines=france_3,
            date_debut=make_aware(datetime.datetime(3021, 2, 19, 17, 10, 41)),
            date_fin=make_aware(datetime.datetime(3022, 2, 19, 17, 10, 41)),
            titre_informatif='titre_pagnol',
            description= 'Un film de Pagnol...',
            date_realisation= 1990,
            public= 18,
            aide_sourd= True,
            note= 5,
            critique= "C'est trop bien",
        )
        gloire.save()

        titre_gloire = Titres.objects.create(programmes_id=gloire.id,
            nom='La gloire de mon Père',
            )
        titre_gloire.save()

        realisateur = Realisateur.objects.create(programmes_id=gloire.id,
            nom="Yves Robert",
            )
        realisateur.save()

        acteur = Acteurs.objects.create(programmes_id=gloire.id,
            nom="Julien CIAMACA",
            role="Marcel Pagnol"
            )
        acteur.save()

        scenariste = Scenariste.objects.create(programmes_id=gloire.id,
            nom="Louis Nucera",
            )
        scenariste.save()

        categorie = Categories.objects.create(nom="film")
        categorie.save()
        categorie.programmes.add(gloire.id)

        series = Series.objects.create(serie=1, episode=2, partie=3,
            programmes_id=gloire.id
            )        
        series.save()

        pays_realisation = PaysRealisation.objects.create(nom="France")
        pays_realisation.save()
        pays_realisation.programmes.add(gloire.id)

        data = urlencode({'chaines_tv': id_france_3,
                         'recherche': 'Marcel',
                         'max_resultats': 4,
                         'titre': 'La gloire de mon Père',
                         'titre_informatif': 'titre_pagnol',
                         'description': 'Un film de Pagnol',
                         'realisateur': 'Robert',
                         'acteur': 'Julien',
                         'role': 'Marcel',
                         'scenariste': 'Louis',
                         'date_realisation': 1990,
                         'categories': 'film',
                         'serie': 1,
                         'episode': 2,
                         'partie': 3,
                         'pays_realisation': 'France',
                         'public': 18,
                         'aide_sourd': True,
                         'note': 5,
                         'critique': "C'est trop bien",
                         })

        response_post = self.client.post(reverse('results'), data, content_type="application/x-www-form-urlencoded")
        assert response_post.status_code == 200
        assert len(response_post.context["info_programmes"]) == 1
        assert response_post.context['info_programmes'][0]['titres'][0].nom == 'La gloire de mon Père'
        assert response_post.context['info_programmes'][0]['chaine'] == 'FRANCE 3'
        assert response_post.context['info_programmes'][0]['programme'].titre_informatif == 'titre_pagnol'
        assert response_post.context['info_programmes'][0]['programme'].description == 'Un film de Pagnol...'
        assert response_post.context['info_programmes'][0]['realisateur'][0].nom =="Yves Robert"
        assert response_post.context['info_programmes'][0]['acteurs'][0].nom == 'Julien CIAMACA'
        assert response_post.context['info_programmes'][0]['acteurs'][0].role == 'Marcel Pagnol'
        assert response_post.context['info_programmes'][0]['scenariste'][0].nom == 'Louis Nucera'
        assert response_post.context['info_programmes'][0]['programme'].date_realisation == 1990
        assert response_post.context['info_programmes'][0]['categories'][0].nom == 'film'
        assert response_post.context['info_programmes'][0]['series'][0].serie == 1
        assert response_post.context['info_programmes'][0]['series'][0].episode == 2
        assert response_post.context['info_programmes'][0]['series'][0].partie == 3
        assert response_post.context['info_programmes'][0]['pays'][0].nom == 'France'
        assert response_post.context['info_programmes'][0]['programme'].aide_sourd == True
        assert response_post.context['info_programmes'][0]['programme'].note == 5
        assert response_post.context['info_programmes'][0]['programme'].critique == "C'est trop bien"
        assert response_post.templates[0].name == "programmes/results.html"

    @mark.django_db
    def test_no_recherche_by_user(self):

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()
        id_france_3 = france_3.id

        data = urlencode({'chaines_tv': id_france_3, 'max_resultats': 4})

        response_post = self.client.post(reverse('results'), data, content_type="application/x-www-form-urlencoded")
        assert response_post.status_code == 200
        assert len(response_post.context["info_programmes"]) == 0
        assert response_post.templates[0].name == "programmes/results.html"

    @mark.django_db
    def test_get_welcom_page(self):

        response_get = self.client.get(reverse('welcome'))

        assert response_get.status_code == 200
        assert response_get.templates[0].name == "programmes/welcome.html"

    @mark.django_db
    def test_bouquet_is_valid(self):

        data = urlencode({'bouquets': 2})

        response_post = self.client.post(reverse('results'), data, content_type="application/x-www-form-urlencoded")

        assert response_post.status_code == 200
        assert response_post.templates[0].name == "programmes/welcome.html"

    @mark.django_db
    def test_bouquet_all_channels(self):

        data = urlencode({'bouquets': 6})

        response_post = self.client.post(reverse('results'), data, content_type="application/x-www-form-urlencoded")

        assert response_post.status_code == 200
        assert response_post.templates[0].name == "programmes/welcome.html"

    @mark.django_db
    def test_bouquet_is_not_valid(self):

        data = urlencode({'bouquets': 7})

        response_post = self.client.post(reverse('results'), data, content_type="application/x-www-form-urlencoded")

        assert response_post.status_code == 302
