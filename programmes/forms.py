from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import BouquetTv, Recherche, RechercheSpecifique, Chaines


class RechercheForm(ModelForm):
    chaines_tv = forms.ModelMultipleChoiceField(
        queryset=Chaines.objects.all().order_by("nom"),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Recherche
        fields = ["recherche", "max_resultats", "chaines_tv"]
        labels = {
            "max_resultats": _("Résultats maximum"),
        }


class BouquetTvForm(ModelForm):
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

    class Meta:
        model = BouquetTv
        fields = ["bouquets"]


class RechercheSpecifiqueForm(ModelForm):

    NOTE_CHOICES = [
        (0, "----"),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    note = forms.ChoiceField(choices=NOTE_CHOICES, required=False)

    class Meta:
        model = RechercheSpecifique
        exclude = ["recherche", "date_debut", "date_fin"]
        labels = {
            "aide_sourd": _("Sous-titres malentendants"),
        }
