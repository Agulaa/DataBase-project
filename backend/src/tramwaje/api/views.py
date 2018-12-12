from rest_framework.generics import  GenericAPIView
from rest_framework.views import APIView
from tramwaje.models import Tramwaj, Linia, Motorniczy, Praca
from .serializers import TramwajSerializer, LiniaSerializer, PracaSerializer, MotorniczySerializer
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, CreateModelMixin
from rest_framework import status
from django.http import Http404
import json 
from django.db import transaction

versions = {}
class test(APIView):
    '''Test praca detail'''
    model_name = "Praca"
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer

    def get(self, request, pk):
        global versions
        try:
            x = Praca.objects.all().filter(id_pracy=pk)
            if self.model_name not in versions:
                versions[self.model_name] = {}
            versions[self.model_name][pk] = x[0].version
            y = PracaSerializer(x[0])
            return Response(y.data)
        except Exception as e:
            return Response({'message': f'{e}'})
            

class PracaView(APIView):
    model_name = "Praca"
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer
    def get(self, request, pk):
        global versions
        try:
            x = Praca.objects.all().filter(id_pracy=pk)
            if self.model_name not in versions:
                versions[self.model_name] = {}
            versions[self.model_name][pk] = x[0].version
            y = PracaSerializer(x[0])
            return Response(y.data)
        except Exception as e:
            return Response({'message': f'{e}'})
    def put(self, request, pk):
        global versions
        updated = Praca.objects.all().filter(id_pracy=pk)[0]

        updated.version = versions[self.model_name][pk] + 1
        try:
            serializer = PracaSerializer(updated, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({'message': f'{e}'})

class PracaViewForOnePerson(APIView):
    model_name = "Praca"
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer
    def get(self, request, id_motorniczego):
        global versions
        try:
            x = Praca.objects.all().filter(id_motorniczego=id_motorniczego)
            all_ = []
            for praca in x:
                y = PracaSerializer(praca)
                all_.append(y.data)
        
            return Response(all_)
        except Exception as e:
            return Response({'message': f'{e}'})
  




class TramwajView(APIView):
    model_name = "Tramwaj"
    queryset = Tramwaj.objects.all()
    serializer_class = TramwajSerializer
    def get(self, request, pk):
        global versions
        try:
            x = Tramwaj.objects.all().filter(id_tramwaju=pk)
            if self.model_name not in versions:
                versions[self.model_name] = {}
            versions[self.model_name][pk] = x[0].version
            y = TramwajSerializer(x[0])
            return Response(y.data)
        except Exception as e:
            return Response({'message': f'{e}'})

    def put(self, request, pk):
        global versions
        updated = Tramwaj.objects.all().filter(id_tramwaju=pk)[0]

        updated.version = versions[self.model_name][pk] + 1
        try:
            serializer = TramwajSerializer(updated, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({'message': f'{e}'})


class LiniaView(APIView):
    model_name = "Linia"
    queryset = Linia.objects.all()
    serializer_class = LiniaSerializer
    def get(self, request, pk):
        global versions
        try:
            x = Linia.objects.all().filter(id_linii=pk)
            if self.model_name not in versions:
                versions[self.model_name] = {}
            versions[self.model_name][pk] = x[0].version
            y = LiniaSerializer(x[0])
            return Response(y.data)
        except Exception as e:
            return Response({'message': f'{e}'})

    def put(self, request, pk):
        global versions
        updated = Linia.objects.all().filter(id_linii=pk)[0]

        updated.version = versions[self.model_name][pk] + 1
        try:
            serializer = LiniaSerializer(updated, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({'message': f'{e}'})



class MotorniczyView(APIView):
    model_name = "Motorniczy"
    queryset = Motorniczy.objects.all()
    serializer_class = MotorniczySerializer

    def get(self, request, pk):
        global versions
        try:
            x = Motorniczy.objects.all().filter(id_motorniczego=pk)
            if self.model_name not in versions:
                versions[self.model_name] = {}
            versions[self.model_name][pk] = x[0].version
            y = MotorniczySerializer(x[0])
            return Response(y.data)
        except Exception as e:
            return Response({'message': f'{e}'})

    def put(self, request, pk):
        global versions
        updated = Motorniczy.objects.all().filter(id_motorniczego=pk)[0]

        updated.version = versions[self.model_name][pk] + 1
        try:
            serializer = MotorniczySerializer(updated, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({'message': f'{e}'})
##view for tabel 

class TramwajListView(ListModelMixin, CreateModelMixin,GenericAPIView):
    queryset = Tramwaj.objects.all()
    serializer_class = TramwajSerializer
    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as e:
            return Response({'message':f'{e}'})
    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({'message':f'{e}'})

 

class LiniaListView(ListModelMixin, CreateModelMixin,GenericAPIView):
    queryset = Linia.objects.all()
    serializer_class = LiniaSerializer
    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as e:
            return Response({'message':f'{e}'})
    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({'message':f'{e}'})
   
class MotorniczyListView(ListModelMixin, CreateModelMixin,GenericAPIView):
    queryset = Motorniczy.objects.all()
    serializer_class = MotorniczySerializer

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as e:
            return Response({'message':f'{e}'})
    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({'message':f'{e}'})

class PracaListView(ListModelMixin, CreateModelMixin,GenericAPIView):


    queryset = Praca.objects.all()
    serializer_class = PracaSerializer

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as e:
            return Response({'message':f'{e}'})

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({'message':f'{e}'})

  


class PracaDetailView(APIView):

    queryset = Praca.objects.all()
    serializer_class = PracaSerializer

    def get(self, request, pk):
            try:
                x = Praca.objects.all().filter(id_pracy=pk)
                y = PracaSerializer(x[0])
                print(self.version)
                self.version = x[0].version
                return Response(y.data)
            except Exception as e:
                return Response({'message': f'{e}'})

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({'message': f'{e}'})

