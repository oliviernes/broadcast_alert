import re
import datetime
import json
import os

from django.conf import settings
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE","broadcast_alert.settings")
import django
django.setup()

from programmes.models import Chaines, Programmes, Titres, Realisateur, Scenariste, Acteurs, Series, Categories, PaysRealisation, Compositeurs

import pdb

class Command(BaseCommand):
    help = "Populate the db with programmes from grabber json file"

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def save(self, data):
        """ Method to save data to the DB. The code that might raise
         an integrity error is wrapped in an atomic block to avoid a 
         TransactionManagementError"""
        try:
            with transaction.atomic():
                data.save()
        except:
            print("The data could not be inserted in the DB.")

    def populate(self, file):
        """Populate the db with the channels and programmes"""

        with open(file, "r") as broadcast:
            data = json.load(broadcast)

        for channel in data["channels"]:
            try:
                chan = Chaines(id_chaine=channel["id"],
                                nom=channel["nom"],
                                icon=channel.get("icon"),
                                url=channel.get("url")
                            )
            except:
                "The channel could not be inserted in the DB"
                continue
            if len(Chaines.objects.filter(id_chaine=channel["id"])) == 0:
                self.save(chan)
                print(f"The channel {chan.nom} has been inserted in the DB")
            else:
                print(f"The channel {chan.nom} has already been inserted in the DB")

        for programme in data['programmes']:
            try:
                chaine = Chaines.objects.get(id_chaine=programme["channel"])
            except:
                print("The programme doesn't have a channel registered in the DB")
                continue
            
            date_d, date_f = programme.get("start", ""), programme.get("stop", "")

            try:
                date_de = [int(date_d[4:12][i:i + 2]) for i in range(0, 8, 2)]
                date_de.insert(0, int(date_d[:4]))
                """The time sent by the teleloisirs API display 60mn instead
                of 1 hour and cannot be use by datetime hence the quick
                fix removing 1mn:"""
                if date_de[4] == 60:
                    date_de[4] = 59
                date_deb = datetime.datetime(date_de[0],
                                            date_de[1],
                                            date_de[2],
                                            date_de[3],
                                            date_de[4]
                                            )
                date_deb = make_aware(date_deb)
            except:
                continue
            try:
                date_fi = [int(date_f[4:12][i:i + 2]) for i in range(0, 8, 2)]
                date_fi.insert(0, int(date_f[:4]))
                if date_fi[4] == 60:
                    date_fi[4] = 59
                date_fin = datetime.datetime(date_fi[0],
                                            date_fi[1],
                                            date_fi[2],
                                            date_fi[3],
                                            date_fi[4]
                                            )
                date_fin = make_aware(date_fin)
            except:
                continue
            
            date_realisation = programme.get("date")

            if date_realisation is not None:
                try:
                    date_realisation = int(date_realisation)
                except:
                    continue

            prog = Programmes(titre_informatif=programme.get("sub-title"),
                                description=programme.get("desc"),
                                date_realisation=date_realisation,
                                icon=programme.get("icon"),
                                url=programme.get("url"),
                                public=programme.get("public"),
                                aide_sourd=programme.get("audio_subtitles"),
                                note=programme.get("note"),
                                critique=programme.get("review"),
                                date_debut=date_deb,
                                date_fin=date_fin,
                                chaines_id=chaine.id
                                )
            try:
                self.save(prog)
            except:
                continue

            try:
                pro = Programmes.objects.get(date_debut=date_deb,
                                    date_fin=date_fin,
                                    chaines_id=chaine.id
                )
            except:
                continue

            titles = programme.get("titles")
            if titles is not None:
                for title in titles:
                    titre = Titres(programmes_id=pro.id, nom=title)
                    self.save(titre)

            directors = programme.get("directors")
            if directors is not None:
                for director in directors:
                    realisateur = Realisateur(programmes_id=pro.id, nom=director)
                    self.save(realisateur)

            writers = programme.get("writers")
            if writers is not None:
                for writer in writers:
                    scenariste = Scenariste(programmes_id=pro.id, nom=writer)
                    self.save(scenariste)

            actors = programme.get("actors")
            if actors is not None:
                for actor in actors:
                    acteur = Acteurs(programmes_id=pro.id,
                                        nom=actor["actor"],
                                        role=actor.get("role")
                    )
                    self.save(acteur)

            episode_num = programme.get("episode-num")

            if episode_num is not None:
                try:
                    episodes = re.split(r'\.', episode_num)
                    serie = re.split('/', episodes[0])[0]
                    episode = re.split('/', episodes[1])[0]
                    partie = re.split('/', episodes[2])[0]
                    if serie == "":
                        serie = None
                    else:
                        serie = int(serie)
                    if episode == "":
                        episode = None
                    else:
                        episode = int(episode)
                    if partie == "":
                        partie = None
                    else:
                        partie = int(partie)
                except:
                    continue
                series = Series(programmes_id=pro.id,
                                serie=serie,
                                episode=episode,
                                partie=partie
                )
                self.save(series)

            composers = programme.get("composers")
            if composers is not None:
                for composer in composers:
                    compositeur = Compositeurs(programmes_id=pro.id, nom=composer)
                    self.save(compositeur)

            categories = programme.get("categories")
            if categories is not None:
                for categorie in categories:
                    if len(Categories.objects.filter(nom=categorie)) != 0:
                        cat = Categories.objects.get(nom=categorie)
                        cat.programmes.add(pro.id)
                    elif categorie.find("/") == -1 and len(Categories.objects.filter(nom=categorie)) == 0:
                        cat = Categories(nom=categorie)
                        try:
                            self.save(cat)
                            cat.programmes.add(pro.id)
                            print(f"The categorie {categorie} has been inserted in the DB.")
                        except:
                            continue

            countries = programme.get("countries")
            if countries is not None:
                for countrie in countries:
                    if len(PaysRealisation.objects.filter(nom=countrie)) != 0:
                        pays = PaysRealisation.objects.get(nom=countrie)
                        pays.programmes.add(pro.id)
                    elif countrie.find("/") == -1 and len(PaysRealisation.objects.filter(nom=countrie)) == 0:
                        pays = PaysRealisation(nom=countrie)
                        try:
                            self.save(pays)
                            pays.programmes.add(pro.id)
                            print(f"The countrie {countrie} has been inserted in the DB.")
                        except:
                            continue

    def handle(self, *args, **options):
        
        self.populate(options['file'][0])
