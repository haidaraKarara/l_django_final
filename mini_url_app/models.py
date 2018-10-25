from django.db import models
import random
import string
#test
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.core.mail import send_mail, mail_admins
from django.utils.translation import ugettext_lazy as _

NOMBRE = 3
#Modèle Mini_url
class MiniURL(models.Model):
    url = models.URLField(verbose_name=_("URL à réduire"),unique=True)
    code = models.CharField(max_length=7,unique=True)
    date = models.DateTimeField(auto_now_add=True,verbose_name=_("Date d'enregistrement"))
    pseudo = models.CharField(max_length=255,blank=True,null=True)
    nb_acces = models.IntegerField(default=0,verbose_name=_("Nombre d'accès à l'URL "))

    def __str__(self):
        return "[{0}] {1}".format(self.code, self.url)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.generer(6)

        super(MiniURL, self).save(*args, **kwargs)

    #fonction pour générer le code correspondant à une url
    def generer(self, nb_caracteres):
        caracteres = string.ascii_letters + string.digits
        aleatoire = [random.choice(caracteres) for _ in range(nb_caracteres)]
        global NOMBRE
        NOMBRE += 1
        aleatoire += str(NOMBRE)
        self.code = ''.join(aleatoire)
    

    class Meta:
        verbose_name = "< Mini URL >"
        verbose_name_plural = "< Minis URL >"
        # permissions = (
        #     ("commenter_article", "Commenter un article"),
        #     ("marquer_article", "Marquer un article comme lu"),
        # )

#TEST

class Eleve(models.Model):
    nom = models.CharField(max_length=31)
    moyenne = models.IntegerField(default=10)

    def __str__(self):
        return "Élève {0} ({1}/20 de moyenne)".format(self.nom, self.moyenne)

class Lieu(models.Model):
    nom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom

class Restaurant(Lieu):
    menu = models.TextField()

from django.db.models.signals import post_delete
from django.dispatch import receiver

# les signaux.. trop cool
# @receiver(post_save, sender=MiniURL)
# def post_save_miniUrl(sender, instance, **kwargs):
# 	#processus de suppression selon les données fournies par instance
#     #print("l'instance {} a été enregistré avec succès!".format(instance))
#     email = EmailMessage(
#         'Hello',
#         'As salam, ceci est un test',
#         'Ababacar Haidara' ,
#         ['ababacarhaidara@gmail.com', 'ababacarhaidara@outlook.com']
#     )
#     try:
#         email.send()
#         mail_admins(
#             "Enregistrement d'une vouvelle URL",
#             "L'URL suivante vient d'être enregistrée : {}".format(instance)
#         )
#     except BaseException as ex:
#         raise(ex)
    