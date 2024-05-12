from django.db import models

# Create your models here.

class Facture(models.Model):
    UTILITY_CHOICES = (
        ('eau', 'Eau'),
        ('gaz', 'Gaz'),
        ('electricite', 'Électricité'),
    )
    typecompt_CHOICES = (
        ('Compteur poignee', 'Compteur poignee'),
        ('Compteur sanitaire', 'Compteur sanitaire'),
    )
    months_CHOICES = (
        ('Janvier','Janvier'),
        ('Février','Février'),
        ('Mars','Mars'),
        ('Avril','Avril'),
        ('Mai','Mai'),
        ('Juin','Juin'),
        ('Juillet','Juillet'),
        ('Aout','Aout'),
        ('Septembre','Septembre'),
        ('Octobre','Octobre'),
        ('Novembre','Novembre'),
        ('Décembre','Décembre')
    )
    utility_type = models.CharField(max_length=20, choices=UTILITY_CHOICES)
    date = models.DateField()
    mois = models.CharField(max_length=20, choices=months_CHOICES)
    annee = models.IntegerField(null=True)
    typecompteur_elec = models.CharField(max_length=20, choices=typecompt_CHOICES, blank=True, null=True)
    consumption = models.FloatField()
    pu = models.FloatField()
    cos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    montant = models.FloatField()

    def __str__(self):
        return f"{self.utility_type} - {self.date}"
    
