from django.db import models

# Create your models here.
class Firmalar(models.Model):
    firma_adi = models.CharField(max_length=100)
    telefon=models.FloatField()
    Adet = models.PositiveIntegerField()
    sha = models.PositiveIntegerField()
    cinsi_1 = models.CharField(max_length=100)
    cinsi_2 = models.CharField(max_length=100)
    renk = models.CharField(max_length=50)
    demir_capi = models.FloatField()
    temiz_capi = models.FloatField()
    boy = models.FloatField()
    kilo = models.FloatField()
    kilo_fiyati = models.DecimalField(max_digits=10, decimal_places=2)
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    durumu=models.TextField()
    not_bilgisi=models.TextField()
    muhasebe_not_bilgisi=models.TextField()
    tarih = models.DateField(auto_now_add=False) 
    
    def __str__(self):
        return self.firma_adi

     
