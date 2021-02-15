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

from .models import Acteurs, Realisateur, Recherche, Programmes, Titres, Scenariste, Categories
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
            selected_ids = []

            titre = form_recherche_specifique.cleaned_data['titre']
            if titre is not None:
                titles = Titres.objects.filter(nom__contains=titre)
                titles_ids = [title.programmes_id for title in titles]
                selected_ids.append(titles_ids)

            titre_informatif = form_recherche_specifique.cleaned_data['titre_informatif']
            if titre_informatif is not None:
                Q_list.append(Q(titre_informatif__contains=titre_informatif))

            description = form_recherche_specifique.cleaned_data['description']
            if description is not None:
                Q_list.append(Q(description__contains=description))

            realisateur = form_recherche_specifique.cleaned_data['realisateur']
            if realisateur is not None:
                directors = Realisateur.objects.filter(nom__contains=realisateur)
                directors_ids = [director.programmes_id for director in directors]
                selected_ids.append(directors_ids)

            acteur = form_recherche_specifique.cleaned_data['acteur']
            if acteur is not None:
                actors = Acteurs.objects.filter(nom__contains=acteur)
                actors_ids = [actor.programmes_id for actor in actors]
                selected_ids.append(actors_ids)

            role = form_recherche_specifique.cleaned_data['role']
            if role is not None:
                roles = Acteurs.objects.filter(role__contains=titre)
                roles_ids = [role.programmes_id for role in roles]
                selected_ids.append(roles_ids)

            scenariste = form_recherche_specifique.cleaned_data['scenariste']
            if scenariste is not None:
                scenaristes = Scenariste.objects.filter(nom__contains=acteur)
                scenaristes_ids = [scenariste.programmes_id for scenariste in scenaristes]
                selected_ids.append(scenaristes_ids)

            date_realisation = form_recherche_specifique.cleaned_data['date_realisation']
            if date_realisation is not None:
                Q_list.append(Q(date_realisation=date_realisation))



            serie = form_recherche_specifique.cleaned_data['serie']
            episode = form_recherche_specifique.cleaned_data['episode']
            partie = form_recherche_specifique.cleaned_data['partie']
            
            public = form_recherche_specifique.cleaned_data['public']
            aide_sourd = form_recherche_specifique.cleaned_data['aide_sourd']
            note = form_recherche_specifique.cleaned_data['note']
            critique = form_recherche_specifique.cleaned_data['critique']
            date_debut = form_recherche_specifique.cleaned_data['date_debut']
            date_fin = form_recherche_specifique.cleaned_data['date_fin']



            match_query_set = []
            match_prog = []

            for chaine in chaines:
                prog_spec = Programmes.objects.filter(reduce(operator.and_, Q_list), chaines=chaine.id)
                if len(prog_spec) > 0:
                    prog_ids = [prog.id for prog in prog_spec]
                    selected_ids.append(prog_ids)

            print(prog_spec)

            programmes_ids = list(set.intersection(*map(set, selected_ids)))

            categorie_ids = []

            categorie = form_recherche_specifique.cleaned_data['categories']
            if categorie is not None:
                for prog_id in programmes_ids:
                    prog = Programmes.objects.get(id=prog_id)
                    categorie_prog = prog.categories_set.all()
                    for cat in categorie_prog:
                        if cat.nom == categorie:
                            categorie_ids.append(prog.id)
                
                programmes_ids = categorie_ids

            pays_ids = []

            pays_realisation = form_recherche_specifique.cleaned_data['pays_realisation']
            if pays_realisation is not None:
                for prog_id in programmes_ids:
                    prog = Programmes.objects.get(id=prog_id)
                    pays_prog = prog.paysrealisation_set.all()
                    for pays in pays_prog:
                        if pays.nom == pays_realisation:
                            pays_ids.append(prog.id)
                
                programmes_ids = pays_ids

            programmes = [Programmes.objects.get(id=prog_id) for prog_id in programmes_ids]


                # if len(prog_spec) > 0:
                #     if len(titles) > 0:
                #         for title in titles:
                #             for prog in prog_spec:
                #                 if title.programmes.id == prog.id:
                #                     match_prog.append(prog)
                #     else:
                #         match_query_set.append(prog_spec)

                # if len(prog_spec) > 0:
                #     if len(foreign_keys) > 0:
                #         for tables in foreign_keys:
                #             for table in tables:
                #                 for prog in prog_spec:
                #                     if table.programmes.id == prog.id:
                #                         match_prog.append(table)
                #     else:
                #         match_query_set.append(prog_spec)


                # if len(prog_spec) > 0:
                #     match.append(prog_spec)

            match_prog = set(match_prog)

            context = {
                # "match_query_set": match_query_set,
                "match": programmes,
                "recherche": f"La recherche  {recherche} n'a donnée aucun résultat pour les 7 prochains jours"
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
