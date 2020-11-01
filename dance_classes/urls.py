from django.urls import path
from .views import dance_classes


urlpatterns = [


    path('courses/',  dance_classes, name='dance-classes')

]