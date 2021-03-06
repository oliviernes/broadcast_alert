from django.core.management.base import BaseCommand

from programmes.models import Recherche, RechercheSpecifique
from programmes.next import ProgrammesNext7D

class Command(BaseCommand):
    help = "Search programmes in the database meeting requirements"

    def search_progs(self):

        searches = Recherche.objects.all()

        for search in searches:
            max_resultats = search.max_resultats
            chaines = search.chaines.all()
            recherche = search.recherche

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


            programmes_7D = ProgrammesNext7D(recherche,
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
                                ).search_7D()

            for prog in programmes_7D:
                search.programmes.add(prog.id)

    def handle(self, *args, **options):

        self.search_progs()
