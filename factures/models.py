from django.db import models
from django.utils import timezone

# Create your models here.

class Facture(models.Model):
    UTILITY_CHOICES = (
        ('eau', 'Eau'),
        ('gaz', 'Gaz'),
        ('electricite', 'Électricité'),
    )
    typecompt_CHOICES = (
        ("Type station d'eau", "Type station d'eau"),
        ("Type sanitaire", "Type sanitaire"),
    )
    typecompte_CHOICES = (
        ('Compteur général', 'Compteur général'),
        ('Munters', 'Munters'),
    )
    months_CHOICES = (
        (1,'Janvier'),
        (2,'Février'),
        (3,'Mars'),
        (4,'Avril'),
        (5,'Mai'),
        (6,'Juin'),
        (7,'Juillet'),
        (8,'Aout'),
        (9,'Septembre'),
        (10,'Octobre'),
        (11,'Novembre'),
        (12,'Décembre')
    )
    utility_type = models.CharField(max_length=20, choices=UTILITY_CHOICES)
    mois = models.IntegerField(choices=months_CHOICES)
    annee = models.IntegerField(null=True)
    typecompteur_eau = models.CharField(max_length=20, choices=typecompt_CHOICES, blank=True, null=True)
    typecompteur_elect = models.CharField(max_length=20, choices=typecompte_CHOICES, blank=True, null=True)
    consumption = models.FloatField()
    pu = models.FloatField()
    cos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    montant = models.FloatField()

    def __str__(self):
        return f"{self.utility_type} - {self.date}"

class ProcessClass(models.Model):
    date = models.DateTimeField(blank=True, null=True,auto_now=True)
    file = models.FileField()