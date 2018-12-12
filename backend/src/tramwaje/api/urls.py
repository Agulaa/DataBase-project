from django.urls import path 
from django.conf.urls import url
from .views import (
    test,
    MotorniczyListView, 
    TramwajListView, 
    LiniaListView, 
    PracaListView, 
    MotorniczyView, 
    TramwajView, 
    LiniaView, 
    PracaView, 
    PracaViewForOnePerson, 
    
  
)




urlpatterns = [
    path('test', test.as_view()),
    path('test/<pk>', test.as_view()),
    path('motorniczy', MotorniczyListView.as_view()),
    path('tramwaj', TramwajListView.as_view()),
    path('praca', PracaListView.as_view()),
    path('linia', LiniaListView.as_view()),
    path('motorniczy/<pk>', MotorniczyView.as_view()),    
    path('tramwaj/<pk>', TramwajView.as_view()),
    path('praca/<pk>', PracaView.as_view()),
    path('linia/<pk>', LiniaView.as_view()),
    path('motorniczy/update/<pk>', MotorniczyView.as_view()),
    path('linia/update/<pk>', LiniaView.as_view()),
    path('praca/update/<pk>', PracaView.as_view()),
    path('tramwaj/update/<pk>', TramwajView.as_view()),
    path('motorniczy/<pk>/delate', MotorniczyView.as_view()),
    path('linia/<pk>/delate', LiniaView.as_view()),
    path('praca/<pk>/delate', PracaView.as_view()),
    path('tramwaj/<pk>/delate', TramwajView.as_view()),
    path('praca/motorniczy/<int:id_motorniczego>', PracaViewForOnePerson.as_view())

]