import os

from django.core.management.base import BaseCommand, CommandError
from config import CHANNELS_TNT
from scraper_alloforfait import Package

os.environ.setdefault("DJANGO_SETTINGS_MODULE","broadcast_alert.settings")
import django
django.setup()

from programmes.models import Chaines, BouquetTv, BouquetsChaines

class Command(BaseCommand):
    help = "Populate the db with package from alloforfait website"

    def add_arguments(self, parser):
        parser.add_argument('package', nargs='+', type=str)

    def save(self, data):
        """ Methode to save data to the DB. The try except block is in a
        while loop to be able to use the loop control statement continue
         which can be used only in a loop"""
        while True:
            try:
                data.save()
                break
            except:
                "The data could not be inserted in the DB"
                continue


    def populate(self, package):
        """Populate the db with channels packages"""

        packages = { 'free' : Package("free").channels(),
                    'sfr' : Package("sfr").channels(),
                    'bouygues' : Package("bbox-bouygues-telecom").channels(),
                    'tnt' : CHANNELS_TNT
        }

        try:
            channels = packages[package]
        except:
            print("You have to choose one of these selected packages: free,"
            "sfr, bouygues or tnt")

        if channels and len(BouquetTv.objects.filter(nom=package)) == 0:
            bouquet = BouquetTv(nom=package)
            self.save(bouquet)
        else:
            bouquet = BouquetTv.objects.get(nom=package)

        for channel in channels:
            chaines = Chaines.objects.filter(nom=channel[1])
            if len(chaines) != 0:
                for chaine in chaines:
                    bouquet_chaine = BouquetsChaines(chaines=chaine,
                                                    bouquettv=bouquet,
                                                    numero=channel[0]
                                                    )
                    self.save(bouquet_chaine)

    def handle(self, *args, **options):
        
        self.populate(options['file'][0])
