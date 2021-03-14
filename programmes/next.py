import operator
import datetime

from functools import reduce

from django.db.models import Q
from django.utils.timezone import make_aware

from .models import Programmes

from .models import (
    Programmes,
    Categories,
    PaysRealisation,
    Scenariste,
    Series,
    Titres,
    Realisateur,
    Acteurs,
)


class ProgrammesNext7D:
    """Provide programmes for the next 7 days according to user's search"""

    def __init__(
        self,
        recherche,
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
    ):
        self.recherche = recherche
        self.max_resultats = max_resultats
        self.chaines = chaines
        self.titre = titre
        self.titre_informatif = titre_informatif
        self.description = description
        self.realisateur = realisateur
        self.acteur = acteur
        self.role = role
        self.scenariste = scenariste
        self.date_realisation = date_realisation
        self.categorie = categorie
        self.serie = serie
        self.episode = episode
        self.partie = partie
        self.pays_realisation = pays_realisation
        self.public = public
        self.aide_sourd = aide_sourd
        self.note = note
        self.critique = critique

    def search_7D(self):

        if self.recherche:

            """Add a Q object to search all related fields"""
            Q_recherche = [
                Q(titres__nom__unaccent__icontains=self.recherche),
                Q(titre_informatif__unaccent__icontains=self.recherche),
                Q(description__unaccent__icontains=self.recherche),
                Q(realisateur__nom__unaccent__icontains=self.recherche),
                Q(acteurs__nom__unaccent__icontains=self.recherche),
                Q(acteurs__role__unaccent__icontains=self.recherche),
                Q(scenariste__nom__unaccent__icontains=self.recherche),
                Q(categories__nom__unaccent__icontains=self.recherche),
                Q(paysrealisation__nom__unaccent__icontains=self.recherche),
                Q(critique__unaccent__icontains=self.recherche),
            ]

        """Add a Q list with Q objects for all related specifique self.recherches"""
        Q_list = []

        if self.titre is not None:
            Q_list.append(Q(titres__nom__unaccent__icontains=self.titre))

        if self.titre_informatif is not None:
            Q_list.append(
                Q(titre_informatif__unaccent__icontains=self.titre_informatif)
            )

        if self.description is not None:
            Q_list.append(Q(description__unaccent__icontains=self.description))

        if self.realisateur is not None:
            Q_list.append(Q(realisateur__nom__unaccent__icontains=self.realisateur))

        if self.acteur is not None:
            Q_list.append(Q(acteurs__nom__unaccent__icontains=self.acteur))

        if self.role is not None:
            Q_list.append(Q(acteurs__role__unaccent__icontains=self.role))

        if self.scenariste is not None:
            Q_list.append(Q(scenariste__nom__unaccent__icontains=self.scenariste))

        if self.date_realisation is not None:
            Q_list.append(Q(date_realisation=self.date_realisation))

        if self.categorie is not None:
            Q_list.append(Q(categories__nom__unaccent__icontains=self.categorie))

        if self.serie is not None:
            Q_list.append(Q(series__serie__icontains=self.serie))

        if self.episode is not None:
            Q_list.append(Q(series__episode__icontains=self.episode))

        if self.partie is not None:
            Q_list.append(Q(series__partie__icontains=self.partie))

        if self.pays_realisation is not None:
            Q_list.append(
                Q(paysrealisation__nom__unaccent__icontains=self.pays_realisation)
            )

        if self.public is not None:
            Q_list.append(Q(public__lte=self.public))

        if self.aide_sourd is not None:
            Q_list.append(Q(aide_sourd=self.aide_sourd))

        if self.note is not None:
            Q_list.append(Q(note__gte=self.note))

        if self.critique is not None:
            Q_list.append(Q(critique__unaccent__icontains=self.critique))

        if len(Q_list) > 0:
            programmes = Programmes.objects.filter(
                reduce(operator.and_, Q_list),
                chaines__in=[chaine.id for chaine in self.chaines],
            ).order_by("date_debut")

        if self.recherche and len(Q_list) == 0:
            programmes = Programmes.objects.filter(
                reduce(operator.or_, Q_recherche),
                chaines__in=[chaine.id for chaine in self.chaines],
            ).order_by("date_debut")
        elif self.recherche and len(Q_list) > 0:
            programmes_recherche = Programmes.objects.filter(
                reduce(operator.or_, Q_recherche),
                id__in=[prog.id for prog in programmes],
            ).order_by("date_debut")
            programmes = programmes_recherche
        elif self.recherche is None and len(Q_list) == 0:
            programmes = []

        """To remove duplicates:"""
        programmes = list(dict.fromkeys(programmes))

        programmes_7D = []

        for progs in programmes:
            if progs.date_debut >= make_aware(datetime.datetime.now()):
                programmes_7D.append(progs)

        programmes_7D = programmes_7D[: self.max_resultats]

        return programmes_7D


class InfoProgrammes:
    """Generate programmes info for template context"""

    def __init__(self, programmes_7D):
        self.programmes_7D = programmes_7D

    def generate_info(self):

        info_programmes = []

        if len(self.programmes_7D) > 0:
            for prog in self.programmes_7D:
                info_prog = {}
                info_prog["programme"] = prog
                info_prog["chaine"] = prog.chaines.nom
                info_prog["titres"] = Titres.objects.filter(programmes_id=prog.id)
                info_prog["realisateur"] = Realisateur.objects.filter(
                    programmes_id=prog.id
                )
                info_prog["scenariste"] = Scenariste.objects.filter(
                    programmes_id=prog.id
                )
                info_prog["acteurs"] = Acteurs.objects.filter(programmes_id=prog.id)
                info_prog["series"] = Series.objects.filter(programmes_id=prog.id)
                info_prog["categories"] = Categories.objects.filter(
                    programmes__id=prog.id
                )
                info_prog["pays"] = PaysRealisation.objects.filter(
                    programmes__id=prog.id
                )
                info_programmes.append(info_prog)

            return info_programmes

        else:
            return info_programmes
