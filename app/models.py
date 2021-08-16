from django.conf import settings
from django.db import models

# Create your models here.

class atletas(models.Model):
    
    code = models.CharField(max_length = 200)
    token_type = models.CharField(max_length = 200)
    expires_at = models.CharField(max_length = 200)
    expires_in = models.CharField(max_length = 200)
    refresh_token = models.CharField(max_length = 200)
    access_token = models.CharField(max_length = 200)
    athlete_id = models.CharField(max_length = 200, unique=True)
    username = models.CharField(max_length = 200)
    resource_state = models.CharField(max_length = 200)
    firstname = models.CharField(max_length = 200)
    lastname = models.CharField(max_length = 200)
    bio = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    country = models.CharField(max_length = 200)
    sex = models.CharField(max_length = 200)
    premium = models.CharField(max_length = 200)
    summit = models.CharField(max_length = 200)
    created_at = models.CharField(max_length = 200)
    updated_at = models.CharField(max_length = 200)
    badge_type_id = models.CharField(max_length = 200)
    weight = models.CharField(max_length = 200)
    profile_medium = models.CharField(max_length = 200)
    profile = models.CharField(max_length = 200)
    friend = models.CharField(max_length = 200)
    follower = models.CharField(max_length = 200)

    class Meta:
        ordering = ["firstname","lastname","athlete_id"]
        verbose_name_plural = "Atletas"

    def __str__(self):
        return (str(self.firstname) + " " + str(self.lastname))

class actividades(models.Model):

    atleta = models.ForeignKey(atletas, on_delete = models.RESTRICT)
    fecha = models.CharField(max_length = 200, null = False)
    año = models.IntegerField(null = False)
    mes = models.IntegerField(null = False)
    dia = models.IntegerField(null = False)
    tipo_choices = (
                    ("Ruta","Ruta"),
                    ("Virtual","Virtual"),
                )
    tipo = models.CharField(choices = tipo_choices, max_length = 200, null = False)
    altura = models.FloatField(null = False)
    cadencia = models.FloatField(null = False)
    distancia = models.FloatField(null = False)
    potencia = models.FloatField(null = False)
    pulsaciones = models.FloatField(null = False)
    tiempo = models.FloatField(null = False)
    velocidad = models.FloatField(null = False)

    class Meta:
        ordering = ["-año","-mes","-dia","-tipo"]
        verbose_name_plural = "Actividades"

    def __str__(self):
        return (str(self.atleta) + " - " + str(self.año) + " - " + str(self.mes) + " - " + str(self.dia) + " - " + str(self.tipo))