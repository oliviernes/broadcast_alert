"""Test views in broadcast app"""
import datetime

from django.utils.timezone import make_aware
from django.forms import forms
from django.test import TestCase, Client
from django.urls import reverse

from unittest.mock import patch
from pytest import mark

from programmes.models import Chaines, Programmes, Titres

from urllib.parse import urlencode

import pdb

class TestResult:

    client = Client()

    @mark.django_db
    def test_no_results_programmes(self):

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()

        data = urlencode({'recherche': 'La gloire de mon Père', 'chaines_tv': 1, 'max_resultats': 4})

        response_post = self.client.post(reverse('results'), data, content_type="application/x-www-form-urlencoded")
        assert response_post.status_code == 200
        assert len(response_post.context["match"]) == 0

    @mark.django_db
    def test_recherche_give_one_results(self):

        france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
        france_3.save()
        gloire = Programmes.objects.create(chaines=france_3,
            date_debut=make_aware(datetime.datetime(3021, 2, 19, 17, 10, 41)),
            date_fin=make_aware(datetime.datetime(3022, 2, 19, 17, 10, 41))
        )
        gloire.save()
        titre_gloire = Titres.objects.create(programmes_id=gloire.id,
            nom='La gloire de mon Père',
            )
        titre_gloire.save()

        data = urlencode({'recherche': 'La gloire de mon Père', 'chaines_tv': 2, 'max_resultats': 4})

        response_post = self.client.post(reverse('results'), data, content_type="application/x-www-form-urlencoded")
        assert response_post.status_code == 200
        assert len(response_post.context["match"]) == 1
        # assert response_post.context['match'][0].titres__nom == 'La gloire de mon Père'

    # @mark.django_db
    # @patch('programmes.views.BouquetTvForm.is_valid')
    # @patch('programmes.views.RechercheForm')
    # @patch('programmes.views.RechercheForm.is_valid')
    # def test_recherche_give_one_results(self,
    #                                      mock_recherche_form_is_valid,
    #                                      mock_recherche_form,
    #                                      mock_bouquettv_form_is_valid
    #                                      ):

    #     france_3 = Chaines.objects.create(id_chaine="france_3", nom="FRANCE 3")
    #     france_3.save()
    #     gloire = Programmes.objects.create(chaines=france_3,
    #         date_debut=make_aware(datetime.datetime(3021, 2, 19, 17, 10, 41)),
    #         date_fin=make_aware(datetime.datetime(3022, 2, 19, 17, 10, 41))
    #     )
    #     gloire.save()
    #     titre_gloire = Titres.objects.create(programmes_id=gloire.id,
    #         nom='La gloire de mon Père',
    #         )
    #     titre_gloire.save()

    #     mock_bouquettv_form_is_valid.return_value = False
    #     mock_recherche_form_is_valid.return_value = True
    #     mock_recherche_form.return_value.cleaned_data = {'recherche': 'La gloire de mon Père', 'max_resultats': 3, 'chaines_tv': france_3}

    #     response_post = self.client.post(reverse('results'))

    #     assert response_post.status_code == 200
    #     assert len(response_post.context["match"]) == 1


# class TestResult(TestCase):

#     def setUp(self):

#         self.client = Client()
#         # self.response_post = self.client.post(reverse('results'), {'recherche': 'La gloire de mon Père', 'chaines_tv': [Chaines.objects.get(nom="FRANCE 3")]})

#     def test_no_results_programmes(self):

#         self.response_post = self.client.post(reverse('results'), {'recherche': 'La gloire de mon Père', 'chaines_tv': [Chaines.objects.get(nom="FRANCE 3")]})
#         # response_post = self.client.post(reverse('results'), {'recherche': 'La gloire de mon Père'})
#         # response_post = self.client.post('results/', {'recherche': 'La gloire de mon Père'})
#         # response_post = self.client.post(reverse('welcome'), {'recherche': 'La gloire de mon Père'})

#         # assert response_post.context["recherche"] == "La recherche 'La gloire de mon Père' n'a donnée aucun résultat pour les 7 prochains jours"

#         self.assertEqual(self.response_post.context["recherche"], "La recherche 'La gloire de mon Père' n'a donnée aucun résultat pour les 7 prochains jours")