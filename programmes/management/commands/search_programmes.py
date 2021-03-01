import operator
import datetime

from functools import reduce

from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand
from django.db.models import Q


from programmes.models import Programmes, Recherche, RechercheSpecifique

class Command(BaseCommand):
    help = "Search programmes in the database meeting requirements"

    def search_progs(self):

        searches = Recherche.objects.all()

        for search in searches:
            max_resultats = search.max_resultats
            chaines = search.chaines.all()
            """Reset recherche to None at the beginning of each loop"""
            recherche = None

            if search.recherche:
                recherche = search.recherche

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

            recherche_spe = RechercheSpecifique.objects.get(recherche_id=search.id)
            
            titre = recherche_spe.titre
            titre_informatif = recherche_spe.titre_informatif
            description = recherche_spe.description
            realisateur = recherche_spe.realisateur
            acteur = recherche_spe.acteur
            role = recherche_spe.role
            scenariste = recherche_spe.scenariste
            date_realisation = recherche_spe.date_realisation
            categorie = recherche_spe.categories
            serie = recherche_spe.serie
            episode = recherche_spe.episode
            partie = recherche_spe.partie
            pays_realisation = recherche_spe.pays_realisation
            public = recherche_spe.public
            aide_sourd = recherche_spe.aide_sourd
            note = recherche_spe.note
            critique = recherche_spe.critique

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
                    chaines__in=[chaine.id for chaine in chaines],
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

            """To  remove duplicates:"""
            programmes = list(dict.fromkeys(programmes))

            programmes_7D = []

            for progs in programmes:
                if progs.date_debut >= make_aware(datetime.datetime.now()):
                    programmes_7D.append(progs)

            programmes_7D = programmes_7D[:max_resultats]

            for prog in programmes_7D:
                search.programmes.add(prog.id)

    def handle(self, *args, **options):
        
        self.search_progs()
