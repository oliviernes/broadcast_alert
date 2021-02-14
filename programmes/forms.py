from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import BouquetTv, Recherche, RechercheSpecifique, Chaines


class RechercheForm(ModelForm):
    chaines_tv = forms.ModelMultipleChoiceField(queryset=Chaines.objects.all().order_by("nom"),
                                                 widget=forms.CheckboxSelectMultiple,
                                                 )
    class Meta:
        model = Recherche
        fields = ['recherche', 'match_all', 'max_resultats', 'chaines_tv']
        # fields = '__all__'

# class RechercheForm(forms.Form):
#     recherche = forms.CharField(max_length=30)

class BouquetTvForm(ModelForm):
    # bouquets = forms.ChoiceField(widget=forms.RadioSelect, choices=[nom.nom for nom in BouquetTv.objects.all()])
    bouquets = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onchange': 'this.form.submit();'}),
                                 choices=[(1, 'Aucunes'),
                                        (2, 'Free'),
                                        (3, 'Sfr'),
                                        (4, 'Bouygues'),
                                        (5, 'TNT'),
                                        (6, 'Toutes les chaînes')]
                                )

    # bouquets = forms.ChoiceField(widget=forms.RadioSelect)

    class Meta:
        model = BouquetTv
        fields = ['bouquets']

class RechercheSpecifiqueForm(ModelForm):

    class Meta:
        model = RechercheSpecifique
        exclude = ['recherche']
        # fields = '__all__'
        # fields = ['titre']
