"""Views to manage programmes"""
import operator
from functools import reduce

from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

# Create your views here.

from .models import Recherche, Programmes
from .forms import RechercheForm, RechercheSpecifiqueForm, BouquetTvForm, Chaines
from config import CHOICES

def welcome(request):
    """Display welcome page"""
    return render(request, "programmes/welcome.html")


# class Results(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'programmes/results.html'

#     def get(self, request):
#         queryset = Programmes.objects.filter((name__contains=query))
#         return Response({'results': queryset[0]})

def search(request):

    if request.method == "POST":
        form_recherche = RechercheForm(request.POST)
        form_bouquet = BouquetTvForm(request.POST)
        form_recherche_specifique = RechercheSpecifiqueForm(request.POST)
        if form_bouquet.is_valid():
            bouquet = form_bouquet.cleaned_data['bouquets']
            if int(bouquet) == 6:
                form_recherche = RechercheForm(initial={'chaines_tv': [chan for chan in Chaines.objects.all()]})
            else:
                form_recherche = RechercheForm(initial={'chaines_tv': [chan for chan in Chaines.objects.filter(bouquettv__nom=CHOICES[int(bouquet)-1])]})
            return render(request, "programmes/welcome.html", {'form_bouquet': form_bouquet,
                                                                'form_recherche': form_recherche,
                                                                'form_recherche_specifique' : form_recherche_specifique
                                                                })

        elif form_recherche.is_valid() and form_recherche_specifique.is_valid():
        # elif form_recherche_specifique.is_valid():

            recherche = form_recherche.cleaned_data['recherche']
            match_all = form_recherche.cleaned_data['match_all']
            max_resultats = form_recherche.cleaned_data['max_resultats']
            chaines = form_recherche.cleaned_data['chaines_tv']

            Q_list = []

            # titre = form_recherche_specifique.cleaned_data['titre']
            # if titre is not None:
            #     Q_list.append(Q(titre__contains=titre))
            titre_informatif = form_recherche_specifique.cleaned_data['titre_informatif']
            if titre_informatif is not None:
                Q_list.append(Q(titre_informatif__contains=titre_informatif))
            description = form_recherche_specifique.cleaned_data['description']
            if description is not None:
                Q_list.append(Q(description__contains=description))
            realisateur = form_recherche_specifique.cleaned_data['realisateur']
            if realisateur is not None:
                Q_list.append(Q(realisateur__contains=realisateur))
            acteur = form_recherche_specifique.cleaned_data['acteur']
            role = form_recherche_specifique.cleaned_data['role']
            scenariste = form_recherche_specifique.cleaned_data['scenariste']
            date_realisation = form_recherche_specifique.cleaned_data['date_realisation']
            categories = form_recherche_specifique.cleaned_data['categories']
            serie = form_recherche_specifique.cleaned_data['serie']
            episode = form_recherche_specifique.cleaned_data['episode']
            partie = form_recherche_specifique.cleaned_data['partie']
            pays_realisation = form_recherche_specifique.cleaned_data['pays_realisation']
            public = form_recherche_specifique.cleaned_data['public']
            aide_sourd = form_recherche_specifique.cleaned_data['aide_sourd']
            note = form_recherche_specifique.cleaned_data['note']
            critique = form_recherche_specifique.cleaned_data['critique']
            date_debut = form_recherche_specifique.cleaned_data['date_debut']
            date_fin = form_recherche_specifique.cleaned_data['date_fin']


            # print(titre)
            # print(titre_informatif)

            match = []
            for chaine in chaines:
                # prog = Programmes.objects.filter(titre_informatif__contains=recherche,
                #                                 chaines=chaine.id)
                # prog_spec = Programmes.objects.filter(titre_informatif__contains=recherche,
                #                                 chaines=chaine.id)
                prog_spec = Programmes.objects.filter(reduce(operator.and_, Q_list), chaines=chaine.id)

                if len(prog_spec) > 0:
                    match.append(prog_spec)
            context = {
                "match": match,
                "recherche": f"La recherche {recherche} n'a donnée aucun résultat pour les 7 prochains jours"
            }
            return render(request, "programmes/results.html", context)

    else:
        form_bouquet = BouquetTvForm()
        form_recherche = RechercheForm()
        form_recherche_specifique = RechercheSpecifiqueForm()

    return render(request, "programmes/welcome.html", {'form_bouquet': form_bouquet,
                                                        'form_recherche': form_recherche,
                                                        'form_recherche_specifique': form_recherche_specifique
                                                         })
