from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from tramwaje.models import Tramwaj, Linia, Motorniczy, Praca, Przeglad
from .serializers import TramwajSerializer, LiniaSerializer, PracaSerializer, MotorniczySerializer, PrzegladSerializer
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from datetime import date, timedelta
from pymongo import * 
import json 
import time 
import datetime 
#from tramwaje.models import User
versions = {}
client = MongoClient('localhost', 27017)
db = client['tramwajeLogi']

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
class PrzegladView(APIView):
    model_name = "Przeglad"
    queryset = Przeglad.objects.all()
    serializer_class = PrzegladSerializer

    def get(self, request, pk):
        global versions
        try:
            x = Przeglad.objects.all().filter(id_przegladu=pk)
            if self.model_name not in versions:
                versions[self.model_name] = {}
            versions[self.model_name][pk] = x[0].version
            y = PrzegladSerializer(x[0])
            db['przeglad'].insert_one(
                {
                    "time": datetime.datetime.utcnow(), 
                    "typerequest":"GET", 
                    "description":f"Wyświetlenie przegladu o id {pk}."
                }
            )
            return Response(y.data)
        except Exception as e:
            return Response({'message': f'{e}'})
    

    def put(self, request, pk):
        global versions
        updated = Przeglad.objects.all().filter(id_przegladu=pk)[0]

        updated.version = versions[self.model_name][pk] + 1
        try:
            serializer = PrzegladSerializer(updated, data=request.data)
            if serializer.is_valid():
                serializer.save()
                db['przeglad'].insert_one(
                {
                    "time": datetime.datetime.utcnow(), 
                    "typerequest":"PUT", 
                    "description":f"Aktualizacja przegladu o id {pk}."
                }
                )
                return Response(serializer.data)
            return Response(serializer.errors)
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
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(), 
                    "typerequest":"GET", 
                    "description":f"Wyświetlenie pracy o id {pk}."
                }
            )
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
                db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(), 
                    "typerequest":"PUT", 
                    "description":f"Aktualizacja pracy o id {pk}."
                }
                )
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({'message': f'{e}'})


class PracaViewForOnePerson(APIView):
    model_name = "Praca"
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer

    def get(self, request, id_motorniczego):
        try:
            x = Praca.objects.all().filter(id_motorniczego=id_motorniczego)
            all_ = []
            for praca in x:
                y = PracaSerializer(praca)
                all_.append(y.data)
                db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(), 
                    "typerequest":"GET", 
                    "description":f"Wyświetlenie pracy dla motorniczego o id {id_motorniczego}."
                }
                )
            return Response(all_)
        except Exception as e:
            return Response({'message': f'{e}'})


class Praca30dayViewForOnePerson(APIView):
    model_name = "Praca"
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer

    def get(self, request, id_motorniczego, datetime_year, datetime_month, datetime_day):
        try:
            start = date(datetime_year, datetime_month, datetime_day)
            end = start + timedelta(days=30)
            x = Praca.objects.all().filter(id_motorniczego=id_motorniczego, poczatekpracy__range=[start, end])
            all_ = []
            for praca in x:
                y = PracaSerializer(praca)
                all_.append(y.data)
                db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(), 
                    "typerequest":"GET", 
                    "description":f"Wyświetlenie pracy dla motorniczego o id {id_motorniczego} z 30 dni od podania daty {datetime_day}.{datetime_month}.{datetime_year}."
                }
                )

            return Response(all_)
        except Exception as e:
            return Response({'message': f'{e}'})


class MotorniczyTopN(APIView):
    model_name = "Praca"
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer

    def get(self, request, n):
        try:
            x = Praca.objects.values('id_motorniczego').annotate(Sum('wynagrodzenie'))[:n]
            all_ = []
            for p in x:
                motorniczy = Motorniczy.objects.all().filter(id_motorniczego=p['id_motorniczego'])

                motorniczy.sum = p['wynagrodzenie__sum']
                y = MotorniczySerializer(motorniczy[0])
                new = dict(y.data)
                new['sum'] = p['wynagrodzenie__sum']
                all_.append(new)
                db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(), 
                    "typerequest":"GET", 
                    "description":f"Wyświetlenie {n} najlepiej zarabiających motorniczych."
                }
                )

            return Response(all_)
        except Exception as e:
            return Response({'message': f'{e}'})

class MotorniczyTopNOkres(APIView):
    model_name = "Praca"
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer

    def get(self, request,datetime_year, quarter):
        try:
            
            if quarter==1:
                start = date(datetime_year, quarter, 1)
                end = date(datetime_year, quarter+2, 31)
            elif quarter==2:
                start = date(datetime_year, quarter*2, 1)
                end = date(datetime_year, quarter*2+2, 30)
            elif quarter==3:
                start = date(datetime_year, quarter*2+1, 1)
                end = date(datetime_year, quarter*2+3, 30)
            else:
                start = date(datetime_year, quarter*2+2, 1)
                end = date(datetime_year, quarter*2+4, 31)
            
            #.values('id_motorniczego').annotate(Sum('wynagrodzenie'))
            a = Praca.objects.all().filter(poczatekpracy__range=[start, end]).aggregate(Sum('wynagrodzenie'))
            print(a)
            x = Praca.objects.all().filter(poczatekpracy__range=[start, end]).values('id_motorniczego').annotate(Sum('wynagrodzenie'))
    
            all_ = []
            for p in x:
                motorniczy = Motorniczy.objects.all().filter(id_motorniczego=p['id_motorniczego'])
                motorniczy.sum = p['wynagrodzenie__sum']
                y = MotorniczySerializer(motorniczy[0])
                new = dict(y.data)
                new['sum'] = p['wynagrodzenie__sum']
                new['okres_od'] = start
                new['okres_do'] = end
                new['caly_zarobek']= a['wynagrodzenie__sum']
                all_.append(new)

            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(), 
                    "typerequest":"GET", 
                    "description":f"Wyświetlenie najlepiej zarabiajacych motorniczych w {quarter} kwartale"
                }
            )

            return Response(all_)
        except Exception as e:
            return Response({'message': f'{e}'})

class TramwajTopN(APIView):
    model_name = "Praca"
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer

    def get(self, request, n):
        try:
            trams = Tramwaj.objects.all()
            all_ = []
            for tram in trams:
                tram_jobs = Praca.objects.all().filter(id_tramwaju=tram.id_tramwaju)
                sum = timedelta()

                for x in tram_jobs:
                    sum += (x.koniecpracy - x.poczatekpracy)
                tramwaj = Tramwaj.objects.all().filter(id_tramwaju=tram.id_tramwaju)
                y = TramwajSerializer(tramwaj[0])
                new = dict(y.data)
                new['sum'] = str(sum)
                all_.append(new)
            newlist = sorted(all_, key=lambda k: k['sum'], reverse=True)[:n]
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "POST",
                    "description": f"Wyświetlenie {n}  najczęściej używanych tramwajów."
                }
            )
            return Response(newlist)
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
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(), 
                    "typerequest":"GET", 
                    "description":f"Wyświetlenie tramwaju o id {pk}"
                }
            )
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
                db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(), 
                    "typerequest":"PUT", 
                    "description":f"Edycja tramwaju o id {pk}"
                }
                 )
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
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(), 
                    "typerequest":"GET", 
                    "description":f"Wyświetlenie linii o id {pk}"
                }
                )
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
                db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(), 
                    "typerequest":"PUT", 
                    "description":f"Edycja linii o id {pk}"
                }
                )
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
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "GET",
                    "description": f"Wyświetlenie {pk} motorniczego"
                }
            )
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
                db['tramwaje'].insert_one(
                    {
                        "time": datetime.datetime.utcnow(),
                        "typerequest": "PUT",
                        "description": f"Edycja {pk} motorniczego"
                    }
                )
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({'message': f'{e}'})


##view for tabel

class TramwajListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Tramwaj.objects.all()
    serializer_class = TramwajSerializer

    def get(self, request, *args, **kwargs):
        try:
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "GET",
                    "description": f"Wyświetlenie tramwajow"
                }
            )
            return self.list(request, *args, **kwargs)
        except Exception as e:
            return Response({'message': f'{e}'})

    def post(self, request, *args, **kwargs):
        try:
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "POST",
                    "description": f"Dodanie tramwaju"
                }
            )
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({'message': f'{e}'})


class LiniaListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Linia.objects.all()
    serializer_class = LiniaSerializer

    def get(self, request, *args, **kwargs):
        try:
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "GET",
                    "description": f"Wyświetlenie linii"
                }
            )
            return self.list(request, *args, **kwargs)
        except Exception as e:
            return Response({'message': f'{e}'})

    def post(self, request, *args, **kwargs):
        try:
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "POST",
                    "description": f"Dodanie linii"
                }
            )
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({'message': f'{e}'})


class MotorniczyListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Motorniczy.objects.all()
    serializer_class = MotorniczySerializer

    def get(self, request, *args, **kwargs):
        try:
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "GET",
                    "description": f"Wyświetlenie motorniczych"
                }
            )
            return self.list(request, *args, **kwargs)
        except Exception as e:
            return Response({'message': f'{e}'})

    def post(self, request, *args, **kwargs):
        try:
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "POST",
                    "description": f"Dodanie motorniczego"
                }
            )
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({'message': f'{e}'})


class PracaListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer

    def get(self, request, *args, **kwargs):
        try:
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "GET",
                    "description": f"Wyświetlenie wszytskich prac."
                }
            )
            return self.list(request, *args, **kwargs)
        except Exception as e:
            return Response({'message': f'{e}'})

    def post(self, request, *args, **kwargs):
        try:
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "POST",
                    "description": f"Dodanie pracy"
                }
            )
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({'message': f'{e}'})

class PrzegladListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Przeglad.objects.all()
    serializer_class = PrzegladSerializer

    def get(self, request, *args, **kwargs):
        try:
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "GET",
                    "description": f"Wyświetlenie wszytskich przegladow."
                }
            )
            return self.list(request, *args, **kwargs)
        except Exception as e:
            return Response({'message': f'{e}'})
    def post(self, request, *args, **kwargs):
        try:
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "POST",
                    "description": f"Dodanie przegladu."
                }
            )
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({'message': f'{e}'})

class PracaDetailView(APIView):
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer

    def get(self, request, pk):
        try:
            x = Praca.objects.all().filter(id_pracy=pk)
            y = PracaSerializer(x[0])
            print(self.version)
            self.version = x[0].version
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "GET",
                    "description": f"Wyświetlenie {pk} pracy"
                }
            )
            return Response(y.data)
        except Exception as e:
            return Response({'message': f'{e}'})

    def post(self, request, *args, **kwargs):
        try:
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "POST",
                    "description": f"Dodanie pracy"
                }
            )
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({'message': f'{e}'})

class PrzegladDetailView(APIView):
    queryset = Przeglad.objects.all()
    serializer_class = PrzegladSerializer

    def get(self, request, fk):
        try:
            x = Przeglad.objects.all().filter(id_tramwaju=fk)
            y = PrzegladSerializer(x[0])
            print(self.version)
            self.version = x[0].version
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "GET",
                    "description": f"Wyświetlenie przegladu dla tramwaju o id {fk}"
                }
            )
            return Response(y.data)
        except Exception as e:
            return Response({'message': f'{e}'})

    def post(self, request, *args, **kwargs):
        try:
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "POST",
                    "description": f"Dodanie przegladu"
                }
            )
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({'message': f'{e}'})





class Statystyki(APIView):
    model_name = "Praca"
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer

    def get(self, request):
        try:
            all_ = []
            trams = Tramwaj.objects.all()
            for tram in trams:
                sum = timedelta()

                tram_jobs = Praca.objects.all().filter(id_tramwaju=tram.id_tramwaju)
                for x in tram_jobs:
                    sum += (x.koniecpracy - x.poczatekpracy)
                tramwaj = Tramwaj.objects.all().filter(id_tramwaju=tram.id_tramwaju)
                y = TramwajSerializer(tramwaj[0])
                new = dict(y.data)
                new['sum'] = str(sum)
                all_.append(new)
            s = sorted(all_, key=lambda k: k['sum'], reverse=True)
            output = []
            output.append(s[0])
            output.append(s[-1])

            all_2 = []
            ppl = Motorniczy.objects.all()
            for person in ppl:
                sum = 0

                person_jobs = Praca.objects.all().filter(id_motorniczego=person.id_motorniczego)
                for x in person_jobs:
                    if x.wynagrodzenie:
                        sum += x.wynagrodzenie
                motorniczy = Motorniczy.objects.all().filter(id_motorniczego=person.id_motorniczego)
                y = MotorniczySerializer(motorniczy[0])
                new = dict(y.data)
                new['sum'] = str(sum)
                all_.append(new)
            s = sorted(all_, key=lambda k: k['sum'], reverse=True)
            output.append(s[0])
            output.append(s[-1])
            db['tramwaje'].insert_one(
                {
                    "time": datetime.datetime.utcnow(),
                    "typerequest": "GET",
                    "description": f"Wyświetlenie statystyk."
                }
            )



            return Response(output)
        except Exception as e:
            return Response({'message': f'{e}'})