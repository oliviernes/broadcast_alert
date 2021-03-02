from django.core.exceptions import NON_FIELD_ERRORS
from django import forms
from django.forms import ModelForm
from .models import BouquetTv, Recherche, RechercheSpecifique, Chaines


class RechercheForm(ModelForm):
    chaines_tv = forms.ModelMultipleChoiceField(
        queryset=Chaines.objects.all().order_by("nom"),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Recherche
        fields = ["recherche", "max_resultats", "chaines_tv"]
        error_messages = {
            NON_FIELD_ERRORS: {"no_channels": "No channels have been ticked"},
        }


# class RechercheForm(forms.Form):
#     recherche = forms.CharField(max_length=30)


class BouquetTvForm(ModelForm):
    # bouquets = forms.ChoiceField(widget=forms.RadioSelect, choices=[nom.nom for nom in BouquetTv.objects.all()])
    bouquets = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"onchange": "this.form.submit();"}),
        choices=[
            (1, "Aucun"),
            (2, "Free"),
            (3, "Sfr"),
            (4, "Bouygues"),
            (5, "TNT"),
            (6, "Toutes les chaînes"),
        ],
    )

    # bouquets = forms.ChoiceField(widget=forms.RadioSelect)

    class Meta:
        model = BouquetTv
        fields = ["bouquets"]


class RechercheSpecifiqueForm(ModelForm):
    class Meta:
        model = RechercheSpecifique
        exclude = ["recherche", "date_debut", "date_fin"]
        # fields = '__all__'
        # fields = ['titre']


class DeleteForm(forms.Form):

    choices = forms.ModelMultipleChoiceField(
        queryset=Recherche.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
