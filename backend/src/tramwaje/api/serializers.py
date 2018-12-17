from rest_framework import serializers
from tramwaje.models import Tramwaj, Linia, Praca, Motorniczy


class TramwajSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tramwaj
        fields = ('id_tramwaju', 'prog_godzinowy', 'aktualny_przebieg')


class LiniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linia
        fields = ('id_linii', 'numer_linii')


class PracaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Praca
        fields = ('id_pracy', 'id_linii', 'id_motorniczego','id_tramwaju', 'poczatekpracy', 'koniecpracy','wynagrodzenie')


class MotorniczySerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorniczy
        fields = ('id_motorniczego', 'imie', 'nazwisko', 'stawka')