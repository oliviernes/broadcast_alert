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
        if form_recherche.is_valid() and form_bouquet.is_valid():
            recherche = form_recherche.cleaned_data['recherche']
            nom = form_bouquet.cleaned_data['nom']
            # match_all = form.cleaned_data['match_all']
            # max_resultats = form.cleaned_data['max_resultats']
            # programmes = form.cleaned_data['programmes']
            # chaines = form.cleaned_data['chaines']
            prog = Programmes.objects.filter(titre_informatif=recherche)

            return render(request, "programmes/results.html", {"prog": prog[0]})

    else:
        form_recherche = RechercheForm(initial={'chaines_tv': [chan for chan in Chaines.objects.filter(nom="6TER")]})
        form_bouquet = BouquetTvForm()
    
    return render(request, "programmes/welcome.html", {'form_bouquet': form_bouquet,
                                                        'form_recherche': form_recherche
                                                         })
