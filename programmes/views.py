"""Views to manage programmes"""
import operator
import datetime

from functools import reduce
from django.utils.timezone import make_aware
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import redirect

# Create your views here.

from .models import Programmes, Chaines
from .forms import RechercheForm, RechercheSpecifiqueForm, BouquetTvForm
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
        breakpoint()
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

        # elif form_recherche.is_valid():
        elif form_recherche.is_valid() and form_recherche_specifique.is_valid():
        # elif form_recherche_specifique.is_valid():
            recherche = form_recherche.cleaned_data['recherche']
            max_resultats = form_recherche.cleaned_data['max_resultats']
            chaines = form_recherche.cleaned_data['chaines_tv']

            Q_recherche = [Q(titres__nom__icontains=recherche),
                            Q(titre_informatif__contains=recherche),
                            Q(description__contains=recherche),
                            Q(realisateur__nom__icontains=recherche),
                            Q(acteurs__nom__icontains=recherche),
                            Q(acteurs__role__icontains=recherche),
                            Q(scenariste__nom__icontains=recherche),
                            Q(categories__nom__icontains=recherche),
                            Q(paysrealisation__nom__icontains=recherche),
                            Q(critique__contains=recherche),
                            ]

            Q_list = []

            titre = form_recherche_specifique.cleaned_data['titre']
            if titre is not None:
                Q_list.append(Q(titres__nom__icontains=titre))

            titre_informatif = form_recherche_specifique.cleaned_data['titre_informatif']
            if titre_informatif is not None:
                Q_list.append(Q(titre_informatif__icontains=titre_informatif))
              
            description = form_recherche_specifique.cleaned_data['description']
            if description is not None:
                 Q_list.append(Q(description__icontains=description))

            realisateur = form_recherche_specifique.cleaned_data['realisateur']
            if realisateur is not None:
                Q_list.append(Q(realisateur__nom__icontains=realisateur))

            acteur = form_recherche_specifique.cleaned_data['acteur']
            if acteur is not None:
                Q_list.append(Q(acteurs__nom__icontains=acteur))

            role = form_recherche_specifique.cleaned_data['role']
            if role is not None:
                Q_list.append(Q(acteurs__role__icontains=role))

            scenariste = form_recherche_specifique.cleaned_data['scenariste']
            if scenariste is not None:
                Q_list.append(Q(scenariste__nom__icontains=scenariste))

            date_realisation = form_recherche_specifique.cleaned_data['date_realisation']
            if date_realisation is not None:
                Q_list.append(Q(date_realisation=date_realisation))

            categorie = form_recherche_specifique.cleaned_data['categories']
            if categorie is not None:
                Q_list.append(Q(categories__nom__icontains=categorie))

            serie = form_recherche_specifique.cleaned_data['serie']
            if serie is not None:
                Q_list.append(Q(series__serie__icontains=serie))

            episode = form_recherche_specifique.cleaned_data['episode']
            if episode is not None:
                Q_list.append(Q(series__episode__icontains=episode))
            
            partie = form_recherche_specifique.cleaned_data['partie']
            if partie is not None:
                Q_list.append(Q(series__partie__icontains=partie))

            pays_realisation = form_recherche_specifique.cleaned_data['pays_realisation']
            if pays_realisation is not None:
                Q_list.append(Q(paysrealisation__nom__icontains=pays_realisation))

            public = form_recherche_specifique.cleaned_data['public']
            if public is not None:
                Q_list.append(Q(public__lte=public))

            aide_sourd = form_recherche_specifique.cleaned_data['aide_sourd']
            if aide_sourd is not None:
                Q_list.append(Q(aide_sourd=aide_sourd))

            note = form_recherche_specifique.cleaned_data['note']
            if note is not None:
                Q_list.append(Q(note__gte=note))

            critique = form_recherche_specifique.cleaned_data['critique']
            if critique is not None:
                Q_list.append(Q(critique__contains=critique))

            date_debut = form_recherche_specifique.cleaned_data['date_debut']
            if date_debut is not None:
                Q_list.append(Q(date_debut__gte=date_debut))

            date_fin = form_recherche_specifique.cleaned_data['date_fin']
            if date_fin is not None:
                Q_list.append(Q(date_fin__lte=date_fin))

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
                    chaines__in=[chaine.id for chaine in chaines]
                ).order_by('date_debut')
                programmes = programmes_recherche
            else:
                programmes = []

            programmes = list(dict.fromkeys(programmes))

            programmes_7D = []

            for progs in programmes:
                if progs.date_debut >= make_aware(datetime.datetime.now()):
                    programmes_7D.append(progs)

            programmes_7D = programmes_7D[:max_resultats]


            context = {
                "match": programmes_7D,
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
