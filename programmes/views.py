"""Views to manage programmes"""
from django.contrib.messages.api import get_messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages

from .next import ProgrammesNext7D, InfoProgrammes

# Create your views here.

from .models import (
    Chaines,
    Recherche,
    RechercheSpecifique,
)
from .forms import RechercheForm, RechercheSpecifiqueForm, BouquetTvForm
from config import CHOICES

import pdb

# def welcome(request):
#     """Display welcome page"""
#     return render(request, "programmes/welcome.html")


# class Results(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'programmes/results.html'

#     def get(self, request):
#         queryset = Programmes.objects.filter((name__contains=query))
#         return Response({'results': queryset[0]})

# def my_search(request):
#     """Display my registered search"""
#     return render(request, "programmes/welcome.html")


def search(request):
    """Display search results for the next 7 days and save user's searches."""
    if request.method == "POST":
        # breakpoint()
        form_recherche = RechercheForm(request.POST)
        form_bouquet = BouquetTvForm(request.POST)
        form_recherche_specifique = RechercheSpecifiqueForm(request.POST)

        if form_bouquet.is_valid():
            bouquet = form_bouquet.cleaned_data["bouquets"]
            if int(bouquet) == 6:
                form_recherche = RechercheForm(
                    initial={"chaines_tv": [chan for chan in Chaines.objects.all()]}
                )
            else:
                form_recherche = RechercheForm(
                    initial={
                        "chaines_tv": [
                            chan
                            for chan in Chaines.objects.filter(
                                bouquettv__nom=CHOICES[int(bouquet) - 1]
                            )
                        ]
                    }
                )
            return render(
                request,
                "programmes/welcome.html",
                {
                    "form_bouquet": form_bouquet,
                    "form_recherche": form_recherche,
                    "form_recherche_specifique": form_recherche_specifique,
                },
            )

        elif form_recherche.is_valid() and form_recherche_specifique.is_valid():

            recherche = form_recherche.cleaned_data["recherche"]
            max_resultats = form_recherche.cleaned_data["max_resultats"]
            chaines = form_recherche.cleaned_data["chaines_tv"]
            titre = form_recherche_specifique.cleaned_data["titre"]
            titre_informatif = form_recherche_specifique.cleaned_data[
                "titre_informatif"
            ]
            description = form_recherche_specifique.cleaned_data["description"]
            realisateur = form_recherche_specifique.cleaned_data["realisateur"]
            acteur = form_recherche_specifique.cleaned_data["acteur"]
            role = form_recherche_specifique.cleaned_data["role"]
            scenariste = form_recherche_specifique.cleaned_data["scenariste"]
            date_realisation = form_recherche_specifique.cleaned_data[
                "date_realisation"
            ]
            categorie = form_recherche_specifique.cleaned_data["categories"]
            serie = form_recherche_specifique.cleaned_data["serie"]
            episode = form_recherche_specifique.cleaned_data["episode"]
            partie = form_recherche_specifique.cleaned_data["partie"]
            pays_realisation = form_recherche_specifique.cleaned_data[
                "pays_realisation"
            ]
            public = form_recherche_specifique.cleaned_data["public"]
            aide_sourd = form_recherche_specifique.cleaned_data["aide_sourd"]
            note = form_recherche_specifique.cleaned_data["note"]
            if note == '0':
                note=None
            critique = form_recherche_specifique.cleaned_data["critique"]

            info_search = {'recherche': recherche,
                        'titre': titre,
                        'titre_informatif': titre_informatif,
                        'description': description,
                        'realisateur': realisateur,
                        'acteur': acteur,
                        'role': role,
                        'scenariste': scenariste,
                        'date_realisation': date_realisation,
                        'categorie': categorie,
                        'serie': serie,
                        'episode': episode,
                        'partie': partie,
                        'pays_realisation': pays_realisation,
                        'public': public,
                        'aide_sourd': aide_sourd,
                        'note': note,
                        'critique': critique,
                        }

            if "my_search" in request.POST:
                """To register user's searches"""
                if request.user.is_authenticated:

                    user_id = request.user.id
                    search = Recherche(
                        recherche=recherche,
                        max_resultats=max_resultats,
                        utilisateur_id=user_id,
                    )

                    search_list = [
                        recherche,
                        titre,
                        titre_informatif,
                        description,
                        realisateur,
                        acteur,
                        role,
                        scenariste,
                        date_realisation,
                        categorie,
                        serie,
                        episode,
                        partie,
                        pays_realisation,
                        public,
                        aide_sourd,
                        note,
                        critique,
                    ]

                    if all(item is None for item in search_list):

                        return render(request, "programmes/no_search.html")

                    else:

                        saved = True

                        try:
                            search.save()
                        except:
                            saved = False

                        specific_search = RechercheSpecifique(
                            recherche_id=search.id,
                            titre=titre,
                            titre_informatif=titre_informatif,
                            description=description,
                            realisateur=realisateur,
                            acteur=acteur,
                            role=role,
                            scenariste=scenariste,
                            date_realisation=date_realisation,
                            categories=categorie,
                            serie=serie,
                            episode=episode,
                            partie=partie,
                            pays_realisation=pays_realisation,
                            public=public,
                            aide_sourd=aide_sourd,
                            note=note,
                            critique=critique,
                        )

                        if saved == True:

                            try:
                                specific_search.save()
                            except:
                                saved = False

                        if saved == True:
                            for chaine in chaines:
                                try:
                                    search.chaines.add(chaine.id)
                                except:
                                    saved = False
                                    break

                        context = {"saved": saved}

                        return render(
                            request, "programmes/registered_info.html", context
                        )

                return redirect("login")

            else:
                """To search the programmes and display the results
                in a new page"""

                programmes_7D = ProgrammesNext7D(recherche,
                                            max_resultats,
                                            chaines,
                                            titre,
                                            titre_informatif,
                                            description,
                                            realisateur,
                                            acteur,
                                            role,
                                            scenariste,
                                            date_realisation,
                                            categorie,
                                            serie,
                                            episode,
                                            partie,
                                            pays_realisation,
                                            public,
                                            aide_sourd,
                                            note,
                                            critique,
                                    ).search_7D()

                info_programmes = InfoProgrammes(programmes_7D).generate_info()

                context = {'info_search': info_search,
                         'info_programmes': info_programmes
                         }
                return render(request, "programmes/results.html", context)

        else:
            messages.add_message(request, messages.INFO, form_recherche.errors)
            return redirect("welcome")

    else:
        storage = get_messages(request)
        form_bouquet = BouquetTvForm()
        form_recherche = RechercheForm()
        form_recherche_specifique = RechercheSpecifiqueForm()

        return render(
            request,
            "programmes/welcome.html",
            {
                "form_bouquet": form_bouquet,
                "form_recherche": form_recherche,
                "form_recherche_specifique": form_recherche_specifique,
                "messages": storage
            },
        )


def my_search(request):
    """Display user's recorded searches"""
    user_id = request.user.id

    recherches = Recherche.objects.filter(utilisateur_id=user_id).order_by("-date_creation")

    searches = []

    for recherche in recherches:
        recherche_specifique = RechercheSpecifique.objects.filter(
            recherche_id=recherche.id
        )
        chaines_list = recherche.chaines.all().order_by("nom")
        chaines_name = [chaine.nom for chaine in chaines_list]
        chaines_string = "\n".join(chaines_name)

        if len(recherche_specifique) > 0:
            searches.append(
                {
                    "recherche": recherche,
                    "recherche_specifique": recherche_specifique[0],
                    "chaines_string": chaines_string,
                }
            )
        else:
            searches.append(
                {
                    "recherche": recherche,
                    "recherche_specifique": None,
                    "chaines_string": chaines_string,
                }
            )

    context = {"searches": searches}

    return render(request, "programmes/my_search.html", context)


def my_results(request, my_search_id):
    """Display user's matching programmes for recorded searches the next 7 days"""

    if request.user.is_authenticated:

        user_id = request.user.id

        recherches = Recherche.objects.filter(utilisateur_id=user_id)

        search_ids = []

        for search in recherches:
            search_ids.append(search.id)

        if my_search_id in search_ids:

            my_search = Recherche.objects.get(id=my_search_id)
            max_resultats = my_search.max_resultats
            chaines = my_search.chaines.all()
            recherche = my_search.recherche

            recherche_spe = RechercheSpecifique.objects.get(recherche_id=my_search.id)

            titre = recherche_spe.titre
            titre_informatif = recherche_spe.titre_informatif
            description = recherche_spe.description
            realisateur = recherche_spe.realisateur
            acteur = recherche_spe.acteur
            role = recherche_spe.role
            scenariste = recherche_spe.scenariste
            date_realisation = recherche_spe.date_realisation
            categorie = recherche_spe.categories
            serie = recherche_spe.serie
            episode = recherche_spe.episode
            partie = recherche_spe.partie
            pays_realisation = recherche_spe.pays_realisation
            public = recherche_spe.public
            aide_sourd = recherche_spe.aide_sourd
            note = recherche_spe.note
            critique = recherche_spe.critique

            info_search = {'recherche': recherche,
                        'titre': titre,
                        'titre_informatif': titre_informatif,
                        'description': description,
                        'realisateur': realisateur,
                        'acteur': acteur,
                        'role': role,
                        'scenariste': scenariste,
                        'date_realisation': date_realisation,
                        'categorie': categorie,
                        'serie': serie,
                        'episode': episode,
                        'partie': partie,
                        'pays_realisation': pays_realisation,
                        'public': public,
                        'aide_sourd': aide_sourd,
                        'note': note,
                        'critique': critique,
                        }

            programmes_7D = ProgrammesNext7D(recherche,
                                        max_resultats,
                                        chaines,
                                        titre,
                                        titre_informatif,
                                        description,
                                        realisateur,
                                        acteur,
                                        role,
                                        scenariste,
                                        date_realisation,
                                        categorie,
                                        serie,
                                        episode,
                                        partie,
                                        pays_realisation,
                                        public,
                                        aide_sourd,
                                        note,
                                        critique,
                                ).search_7D()

            info_programmes = InfoProgrammes(programmes_7D).generate_info()


            context = {'info_search': info_search,
                        'info_programmes': info_programmes
                        }
            return render(request, "programmes/results.html", context)
        else:
            return render(request, "programmes/no_results.html")
    else:
        return render(request, "programmes/auth_info.html")

def delete(request, pk):
    # breakpoint()

    if request.user.is_authenticated:

        user_id = request.user.id

        recherches = Recherche.objects.filter(utilisateur_id=user_id)

        search_ids = []

        for search in recherches:
            search_ids.append(search.id)

        if pk in search_ids:
        
            item = Recherche.objects.get(id=pk)
            item.delete()

            if request.is_ajax():
                data = {
                        'my_data': "data_to_give_to_fetch"
                }
                return JsonResponse(data)
            else:
                return render(request, "programmes/welcome.html")
        else:
            return render(request, "programmes/not_delete.html")
    else:
        return render(request, "programmes/auth_info.html")