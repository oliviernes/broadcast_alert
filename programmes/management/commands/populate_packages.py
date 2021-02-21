import os

from django.core.management.base import BaseCommand, CommandError
from config import CHANNELS_TNT
from scraper_alloforfait import Package
from django.db import transaction


os.environ.setdefault("DJANGO_SETTINGS_MODULE","broadcast_alert.settings")
import django
django.setup()

from programmes.models import Chaines, BouquetTv, BouquetsChaines

class Command(BaseCommand):
    help = "Populate the db with package from alloforfait website"

    def add_arguments(self, parser):
        parser.add_argument('package', nargs='+', type=str)

    def save(self, data):
        """ Method to save data to the DB. The code that might raise
         an integrity error is wrapped in an atomic block to avoid a 
         TransactionManagementError"""
        try:
            with transaction.atomic():
                data.save()
        except:
            print("The data could not be inserted in the DB.")
            data.delete()


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
            channels = False
            print("You have to choose one of these selected packages: free,"
            "sfr, bouygues or tnt")

        if channels:
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

        self.populate(options['package'][0])
