from django.db import models

class Dimensiones(models.Model):
    lpn = models.CharField(max_length=255, primary_key=True)
    largo = models.FloatField()
    alto = models.FloatField()
    ancho = models.FloatField()

    def __str__(self):
        return f"LPN: {self.lpn}, Largo: {self.largo}, Alto: {self.alto}, Ancho: {self.ancho}"