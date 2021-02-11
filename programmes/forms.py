from django import forms
from django.db.models import fields
from django.forms import ModelForm, CheckboxSelectMultiple
from .models import BouquetTv, Recherche, Chaines


class RechercheForm(ModelForm):
    chaines_tv = forms.ModelMultipleChoiceField(queryset=Chaines.objects.all().order_by("nom"),
                                                 widget=forms.CheckboxSelectMultiple,
                                                #  initial={'chaines':[chan for chan in Chaines.objects.all().values_list('id_chaine', flat=True)]}
                                                # initial={'nom': Chaines.objects.filter(nom="6TER")}
                                                 )
    class Meta:
        model = Recherche
        fields = ['recherche', 'match_all', 'max_resultats', 'chaines_tv']
        # fields = '__all__'
        # widgets = {
        #     'chaines': CheckboxSelectMultiple(),
        #     'field2': CheckboxSelectMultiple()
        # }

# class RechercheForm(forms.Form):
#     recherche = forms.CharField(max_length=30)

class BouquetTvForm(ModelForm):
    class Meta:
        model = BouquetTv
        fields = ['nom']
