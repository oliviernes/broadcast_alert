import datetime
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from django.core.mail import send_mail

from programmes.models import Programmes, Recherche, Chaines

class Command(BaseCommand):
    help = "Search programmes in the database meeting requirements"

    def send_email(self):

        users = User.objects.all()

        for user in users:

            searches = Recherche.objects.filter(utilisateur_id=user.id)

            for search in searches:
                prog_match = search.programmes.all()
                new_prog = []
                week_prog = []
                if len(prog_match) > 0:
                    for prog in prog_match:
                        # if prog.date_debut > make_aware(datetime.datetime.now() + timedelta(6)):
                        if prog.date_debut > make_aware(datetime.datetime.now() + timedelta(1)):                        
                            new_prog.append(prog)
                        elif make_aware(datetime.datetime.now() < prog.date_debut < make_aware(datetime.datetime.now() + timedelta(6))):
                            week_prog.append(prog)
                # if search.date_creation < make_aware(datetime.datetime.now() - timedelta(7)):
                if search.date_creation < make_aware(datetime.datetime.now()):
                    if len(new_prog) == 1:
                        chaine = Chaines.objects.get(id=new_prog[0].chaines_id)
                        subject = "Un programme correspond à votre recherche!"
                        message = f"Votre recherche créée le {search.date_creation} a obtenu un résultat: {new_prog[0].titres_set.all()[0]}, le {new_prog[0].date_debut} sur la chaîne {chaine.nom}"
                        send_mail(subject, message, 'popular.crazy2@gmail.com', [user.email])

    def handle(self, *args, **options):
        
        self.send_email()
