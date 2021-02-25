from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail

class TestResetPassword(TestCase):

    def setUp(self):

        self.client = Client()
        user = User.objects.create_user("Mell", "mell2010@gmail.com", "1234simplepassword")
        self.response_post = self.client.post(reverse('password_reset'),{'email':'mell2010@gmail.com'})
        self.token = self.response_post.context[0]['token']
        self.uid = self.response_post.context[0]['uid']

    def test_get_reset_password_form(self):

        response = self.client.get(reverse('reset_password'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["registration/password_reset.html"])

    def test_sending_email_to_reset_password(self):

        self.assertEqual(self.response_post.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Réinitialisation du mot de passe sur testserver")

    def test_get_password_change_form(self):

        response = self.client.get(reverse
                                    ('password_reset_confirm',
                                    kwargs={'token':self.token,'uidb64':self.uid}
                                    ), follow=True
                                )

        assert response.status_code == 200
        assert response.template_name == ["registration/password_reset_form.html"]

    def test_get_change_password(self):

        response = self.client.post(reverse
                                    ('password_reset_confirm',
                                    kwargs={'token':self.token,'uidb64':self.uid}
                                    ),
                                    {'new_password1':'simplepassword1234',
                                    'new_password2':'simplepassword1234'}
                                    )
        assert response.status_code == 302

    def test_get_password_done(self):

        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["registration/password_reset_done.html"])
