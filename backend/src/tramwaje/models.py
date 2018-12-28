from django.db import models
from datetime import datetime    
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Przeglad(models.Model):
    id_przegladu = models.AutoField(db_column='ID_Przegladu', primary_key=True)  # Field name made lowercase.
    id_tramwaju = models.ForeignKey('Tramwaj', models.DO_NOTHING, db_column='ID_Tramwaju'
                                    )  # Field name made lowercase.
    date = models.DateTimeField(db_column='Data', default=datetime.now, blank=True)
  
    class Meta:
        managed = False
        db_table = 'przeglad'



class Linia(models.Model):
    id_linii = models.AutoField(db_column='ID_Linii', primary_key=True)  # Field name made lowercase.
    numer_linii = models.IntegerField(db_column='Numer_Linii')  # Field name made lowercase.
    version = models.IntegerField(default=0)
    class Meta:
        managed = False
        db_table = 'linia'


class Motorniczy(models.Model):
    id_motorniczego = models.AutoField(db_column='ID_Motorniczego', primary_key=True)  # Field name made lowercase.
    imie = models.CharField(db_column='Imie', max_length=45)  # Field name made lowercase.
    nazwisko = models.CharField(db_column='Nazwisko', max_length=45)  # Field name made lowercase.
    stawka = models.FloatField(db_column='Stawka')  # Field name made lowercase.
    zatrudniony = models.TextField(db_column='Zatrudniony',
                                   default=1)  # Field name made lowercase. This field type is a guess.
    version = models.IntegerField(default=0)
    class Meta:
        managed = False
        db_table = 'motorniczy'


class Praca(models.Model):
    id_pracy = models.AutoField(db_column='ID_Pracy', primary_key=True)  # Field name made lowercase.
    id_linii = models.ForeignKey(Linia, models.DO_NOTHING, db_column='ID_Linii')  # Field name made lowercase.
    id_motorniczego = models.ForeignKey(Motorniczy, models.DO_NOTHING,
                                        db_column='ID_Motorniczego')  # Field name made lowercase.
    id_tramwaju = models.ForeignKey('Tramwaj', models.DO_NOTHING, db_column='ID_Tramwaju'
                                    )  # Field name made lowercase.
    poczatekpracy = models.DateTimeField(db_column='PoczatekPracy')  # Field name made lowercase.
    koniecpracy = models.DateTimeField(db_column='KoniecPracy', blank=True, null=True)  # Field name made lowercase.
    wynagrodzenie = models.FloatField(db_column='Wynagrodzenie', blank=True, null=True)  # Field name made lowercase.
    version = models.IntegerField(default=0)
    class Meta:
        managed = False
        db_table = 'praca'


class Tramwaj(models.Model):
    id_tramwaju = models.AutoField(db_column='ID_Tramwaju', primary_key=True)  # Field name made lowercase.
    prog_godzinowy = models.IntegerField(db_column='Prog_Godzinowy')  # Field name made lowercase.
    aktualny_przebieg = models.FloatField(db_column='Aktualny_Przebieg')  # Field name made lowercase.
    version = models.IntegerField(default=0)
    class Meta:
        managed = False
        db_table = 'tramwaj'