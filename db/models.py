import sys

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()


class Register(models.Model):
    ism = models.CharField(max_length=200)
    familya = models.CharField(max_length=200)
    telefon_nomer = models.CharField(max_length=200)
    kurs = models.CharField(max_length=200)
    vaqt = models.CharField(max_length=200)
    registratsiya_vaqti = models.DateField(auto_now_add=True, blank=True, null=True)
