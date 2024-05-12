from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class WaterConsumption(models.Model):
    date = models.DateField()
    meter_reading = models.IntegerField()
    daily_consumption = models.IntegerField()
    
    
class EnergyConsumption(models.Model):
    date = models.DateField()
    meter_reading = models.IntegerField()
    daily_consumption = models.IntegerField()

class WaterMonthlyConsumption(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    old_meter = models.IntegerField()
    new_meter = models.IntegerField()
    prix_u_old = models.FloatField()

class EnergyMonthlyConsumption(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    old_meter = models.IntegerField()
    new_meter = models.IntegerField()
    prix_u_old = models.FloatField()


class Munters(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    elec_consumption = models.FloatField()
    munters_consumption = models.FloatField()
    facture_DTTC = models.FloatField()
    elec_munters_DTTC = models.FloatField()
    
class Machines(models.Model):
    nom = models.TextField()
    panne = models.TextField()

class GasConsumption(models.Model):
    date = models.DateField()
    meter_reading = models.IntegerField()
    daily_consumption = models.IntegerField()

class GasMonthlyConsumption(models.Model):
    month = models.IntegerField()
    
    year = models.IntegerField()
    old_meter = models.IntegerField()
    new_meter = models.IntegerField()
    prix_u_old = models.FloatField()
