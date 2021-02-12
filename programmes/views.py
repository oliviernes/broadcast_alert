"""Views to manage programmes"""
from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

from .models import Recherche, Programmes
from .forms import RechercheForm, BouquetTvForm, Chaines
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
        if form_bouquet.is_valid():
            bouquet = form_bouquet.cleaned_data['bouquets']
            if int(bouquet) == 6:
                form_recherche = RechercheForm(initial={'chaines_tv': [chan for chan in Chaines.objects.all()]})
            else:
                form_recherche = RechercheForm(initial={'chaines_tv': [chan for chan in Chaines.objects.filter(bouquettv__nom=CHOICES[int(bouquet)-1])]})
            return render(request, "programmes/welcome.html", {'form_bouquet': form_bouquet,
                                                                'form_recherche': form_recherche
                                                                })

        elif form_recherche.is_valid():
            recherche = form_recherche.cleaned_data['recherche']
            match_all = form_recherche.cleaned_data['match_all']
            max_resultats = form_recherche.cleaned_data['max_resultats']
            chaines = form_recherche.cleaned_data['chaines_tv']
            print(chaines)
            match = []
            for chaine in chaines:
                prog = Programmes.objects.filter(titre_informatif__contains=recherche,
                                                chaines=chaine.id)
                if len(prog) > 0:
                    match.append(prog)
            context = {
                "match": match,
                "recherche": f"La recherche {recherche} n'a donnée aucun résultat pour les 7 prochains jours"
            }
            return render(request, "programmes/results.html", context)

    else:
        form_bouquet = BouquetTvForm()
        form_recherche = RechercheForm()
    
    return render(request, "programmes/welcome.html", {'form_bouquet': form_bouquet,
                                                        'form_recherche': form_recherche
                                                         })
