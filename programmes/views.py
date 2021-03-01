"""Views to manage programmes"""
import operator
import datetime

from functools import reduce
from django.utils.timezone import make_aware
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.models import User

# Create your views here.

from .models import Categories, PaysRealisation, Programmes, Chaines, Recherche, RechercheSpecifique, Scenariste, Series, Titres, Realisateur, Acteurs
from .forms import DeleteForm, RechercheForm, RechercheSpecifiqueForm, BouquetTvForm
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

            recherche = form_recherche.cleaned_data['recherche']
            max_resultats = form_recherche.cleaned_data['max_resultats']
            chaines = form_recherche.cleaned_data['chaines_tv']
            titre = form_recherche_specifique.cleaned_data['titre']
            titre_informatif = form_recherche_specifique.cleaned_data['titre_informatif']
            description = form_recherche_specifique.cleaned_data['description']
            realisateur = form_recherche_specifique.cleaned_data['realisateur']
            acteur = form_recherche_specifique.cleaned_data['acteur']
            role = form_recherche_specifique.cleaned_data['role']
            scenariste = form_recherche_specifique.cleaned_data['scenariste']
            date_realisation = form_recherche_specifique.cleaned_data['date_realisation']
            categorie = form_recherche_specifique.cleaned_data['categories']
            serie = form_recherche_specifique.cleaned_data['serie']
            episode = form_recherche_specifique.cleaned_data['episode']
            partie = form_recherche_specifique.cleaned_data['partie']
            pays_realisation = form_recherche_specifique.cleaned_data['pays_realisation']
            public = form_recherche_specifique.cleaned_data['public']
            aide_sourd = form_recherche_specifique.cleaned_data['aide_sourd']
            note = form_recherche_specifique.cleaned_data['note']
            critique = form_recherche_specifique.cleaned_data['critique']


            if 'my_search' in request.POST:
                """To register user's searches"""
                if request.user.is_authenticated:

                    user_id = request.user.id
                    search = Recherche(recherche=recherche,
                                                max_resultats=max_resultats,
                                                utilisateur_id=user_id
                                                )

                    search_list = [ recherche,
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


                        specific_search = RechercheSpecifique(recherche_id=search.id,
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
                                search.chaines.add(chaine.id)

                        context = {
                            'saved': saved
                        }

                        return render(request, "programmes/registered_info.html", context)

                return redirect("login")

            else:
                """To search the programmes and display the results
                in a new page"""

                """Add a Q object to search all related fields"""
                Q_recherche = [Q(titres__nom__icontains=recherche),
                                Q(titre_informatif__icontains=recherche),
                                Q(description__icontains=recherche),
                                Q(realisateur__nom__icontains=recherche),
                                Q(acteurs__nom__icontains=recherche),
                                Q(acteurs__role__icontains=recherche),
                                Q(scenariste__nom__icontains=recherche),
                                Q(categories__nom__icontains=recherche),
                                Q(paysrealisation__nom__icontains=recherche),
                                Q(critique__icontains=recherche),
                                ]

                """Add a Q list with Q objects for all related specifique recherches"""
                Q_list = []

                if titre is not None:
                    Q_list.append(Q(titres__nom__icontains=titre))

                if titre_informatif is not None:
                    Q_list.append(Q(titre_informatif__icontains=titre_informatif))

                if description is not None:
                    Q_list.append(Q(description__icontains=description))

                if realisateur is not None:
                    Q_list.append(Q(realisateur__nom__icontains=realisateur))

                if acteur is not None:
                    Q_list.append(Q(acteurs__nom__icontains=acteur))

                if role is not None:
                    Q_list.append(Q(acteurs__role__icontains=role))

                if scenariste is not None:
                    Q_list.append(Q(scenariste__nom__icontains=scenariste))

                if date_realisation is not None:
                    Q_list.append(Q(date_realisation=date_realisation))

                if categorie is not None:
                    Q_list.append(Q(categories__nom__icontains=categorie))

                if serie is not None:
                    Q_list.append(Q(series__serie__icontains=serie))

                if episode is not None:
                    Q_list.append(Q(series__episode__icontains=episode))

                if partie is not None:
                    Q_list.append(Q(series__partie__icontains=partie))

                if pays_realisation is not None:
                    Q_list.append(Q(paysrealisation__nom__icontains=pays_realisation))

                if public is not None:
                    Q_list.append(Q(public__lte=public))

                if aide_sourd is not None:
                    Q_list.append(Q(aide_sourd=aide_sourd))

                if note is not None:
                    Q_list.append(Q(note__gte=note))

                if critique is not None:
                    Q_list.append(Q(critique__icontains=critique))


                if len(Q_list) > 0:
                    programmes = Programmes.objects.filter(
                        reduce(operator.and_, Q_list),
                        chaines__in=[chaine.id for chaine in chaines]
                    ).order_by('date_debut')


                if recherche and len(Q_list) == 0:
                    programmes = Programmes.objects.filter(
                        reduce(operator.or_, Q_recherche),
                        chaines__in=[chaine.id for chaine in chaines]
                    ).order_by('date_debut')
                elif recherche and len(Q_list) > 0:
                    programmes_recherche = Programmes.objects.filter(
                        reduce(operator.or_, Q_recherche),
                        id__in=[prog.id for prog in programmes],
                    ).order_by('date_debut')
                    programmes = programmes_recherche
                elif recherche is None and len(Q_list) == 0:
                    programmes = []


                """To remove duplicates:"""
                programmes = list(dict.fromkeys(programmes))

                programmes_7D = []

                for progs in programmes:
                    if progs.date_debut >= make_aware(datetime.datetime.now()):
                        programmes_7D.append(progs)

                programmes_7D = programmes_7D[:max_resultats]

                info_programmes = []

                if len(programmes_7D) > 0:
                    for prog in programmes_7D:
                        info_prog = {}
                        info_prog['programme'] = prog
                        info_prog['chaine'] = prog.chaines.nom
                        info_prog['titres'] = Titres.objects.filter(programmes_id=prog.id)
                        info_prog['realisateur'] = Realisateur.objects.filter(programmes_id=prog.id)
                        info_prog['scenariste'] = Scenariste.objects.filter(programmes_id=prog.id)
                        info_prog['acteurs'] = Acteurs.objects.filter(programmes_id=prog.id)
                        info_prog['series'] = Series.objects.filter(programmes_id=prog.id)
                        info_prog['categories'] = Categories.objects.filter(programmes__id=prog.id)
                        info_prog['pays'] = PaysRealisation.objects.filter(programmes__id=prog.id)
                        info_programmes.append(info_prog)

                context = {
                    'info_programmes': info_programmes
                }
                return render(request, "programmes/results.html", context)

        else:
            form_bouquet = BouquetTvForm()
            form_recherche = RechercheForm()
            form_recherche_specifique = RechercheSpecifiqueForm()

            return redirect('welcome')

    else:
        form_bouquet = BouquetTvForm()
        form_recherche = RechercheForm()
        form_recherche_specifique = RechercheSpecifiqueForm()

        return render(request, "programmes/welcome.html", {'form_bouquet': form_bouquet,
                                                            'form_recherche': form_recherche,
                                                            'form_recherche_specifique': form_recherche_specifique
                                                            })

def my_search(request):
    """Display user's recorded searches and delete selected searches"""
    user_id = request.user.id

    recherches = Recherche.objects.filter(utilisateur_id=user_id)

    searches=[]

    for recherche in recherches:
        recherche_specifique = RechercheSpecifique.objects.filter(recherche_id=recherche.id)
        chaines_list = recherche.chaines.all().order_by("nom")
        chaines_name = [chaine.nom for chaine in chaines_list]
        chaines_string = '-'.join(chaines_name)

        if len(recherche_specifique) > 0:
            searches.append({'recherche': recherche,
                             'recherche_specifique': recherche_specifique[0],
                             'chaines_string': chaines_string
                             })
        else:
            searches.append({'recherche': recherche,
                             'recherche_specifique': None,
                             'chaines_string': chaines_string
                             })

    if request.method == "POST":
        form_delete = DeleteForm(request.POST)

        if form_delete.is_valid() and 'delete' in request.POST:
            for selected_search in form_delete.cleaned_data['choices']:
                selected_search.delete()

            return redirect('my_search')
        else:
            return redirect('my_search')
    else:
        form_delete = DeleteForm()

        context = {
            'searches': searches,
            'form_delete': form_delete
        }

        return render(request, "programmes/my_search.html", context)

