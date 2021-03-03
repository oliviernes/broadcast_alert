import datetime
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from programmes.models import Programmes, Recherche, Chaines

import pdb

class Command(BaseCommand):
    help = "Search programmes in the database meeting requirements"

    def send_email(self):

        users = User.objects.all()
        # users = User.objects.all()[:1]

        for user in users:

            searches = Recherche.objects.filter(utilisateur_id=user.id)

            infos_mail = []
            email_to_send = False

            for search in searches:
                prog_match = search.programmes.all()
                new_prog = []
                old_prog = []
                if len(prog_match) > 0:
                    for prog in prog_match:
                        titres = prog.titres_set.all()
                        if len(titres) > 0:
                            titre = titres[0].nom
                            # if prog.date_debut > make_aware(datetime.datetime.now() + timedelta(6)):
                            if prog.date_debut > make_aware(datetime.datetime.now() + timedelta(5)):
                                new_prog.append({'prog': prog,
                                                'chaine': Chaines.objects.get(id=prog.chaines_id),
                                                'titre': titre
                                                })
                                email_to_send = True
                            if make_aware(datetime.datetime.now()) < prog.date_debut < make_aware(datetime.datetime.now()) + timedelta(5):
                                old_prog.append({'prog': prog,
                                                'chaine': Chaines.objects.get(id=prog.chaines_id),
                                                'titre': titre
                                })
                # if search.date_creation < make_aware(datetime.datetime.now() - timedelta(7)):
                if search.date_creation < make_aware(datetime.datetime.now()):
                    infos_search = { "search": search,
                        'new_prog': new_prog,
                        'old_prog': old_prog
                    }
                    infos_mail.append(infos_search)

            if email_to_send:
                if len(infos_mail) == 1:
                    if len(infos_mail[0]['new_prog']) == 1:
                        subject = "Un programme correspond à votre recherche!"
                    elif len(infos_mail[0]['new_prog']) > 1:
                        subject = "Des programmes correspondent à votre recherche!"
                elif len(infos_mail) > 1:
                    subject = "Des programmes correspondent à vos recherches!"

                context = { 'infos_mail': infos_mail }

                from_email, to = 'popular.crazy2@gmail.com', user.email,

                text_content = render_to_string('programmes/email.txt', context)
                html_content = render_to_string('programmes/email.html', context)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()


    def handle(self, *args, **options):
        
        self.send_email()
