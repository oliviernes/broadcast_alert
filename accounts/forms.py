from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Class to signup users"""

    first_name = forms.CharField(
        label="Prénom", max_length=30, required=True, help_text="Requis."
    )
    last_name = forms.CharField(
        label="Nom", max_length=30, required=False, help_text="Optionel."
    )
    email = forms.EmailField(
        label="Courriel",
        max_length=254,
        help_text="Requis. Entrez une adresse email valide.",
    )

    def clean_email(self):
        """Validation error for emails"""
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError(
                "L'adresse email est déjà enregistrée."
                " Veuillez renseigner une autre adresse email."
            )
        return self.cleaned_data["email"]

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class EmailLoginForm(AuthenticationForm):
    """Class to add label to username field"""

    username = UsernameField(
        label="Adresse Email", widget=forms.TextInput(attrs={"autofocus": True}),
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Saisissez un email et un mot de passe valides. Remarquez que chacun de ces champs est sensible à la casse (différenciation des majuscules/minuscules)."
                )
        return self.cleaned_data
