from os.path import exists

from .models import MiniURL
from django.test import TestCase
from django.urls import reverse
from django.test import Client


def creer_url():
    mini = MiniURL(url="http://foo.bar",code='12457pl', pseudo="Maxime")
    mini.save()
    return mini

class MiniURLTests(TestCase):
    def test_liste(self):
        """ Vérifie si une URL sauvegardée est bien affichée """
    
        mini = creer_url()
        reponse = self.client.get(reverse('url_liste'))
        self.assertEqual(reponse.status_code,200)
        self.assertContains(reponse, mini.url)
        self.assertQuerysetEqual(reponse.context['minis'], [repr(mini)])

    def test_nouveau_redirection(self):
        """ Vérifie la redirection d'un ajout d'URL """
        c = Client()
        c.login(username="admin",password="passer1234")
        data = {
            'url': 'http://www.djangoproject.com',
            'pseudo': 'Jean Dupont',
        }

        reponse = self.client.post(reverse('url_nouveau'), data)
        self.assertEqual(reponse.status_code, 302)
        self.assertRedirects(reponse,'/m/connexion?next=/m/nouveau')
        reponse = c.get(reverse('url_liste'))
        self.assertEqual(reponse.status_code,200)

