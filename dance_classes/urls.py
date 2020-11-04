from django.urls import path
from .views import dance_classes, add_dance_class, edit_dance_class, dance_class_detail


urlpatterns = [


    path('courses/',  dance_classes, name='dance-classes'),
    path('add-dance-class/', add_dance_class, name='add-dance-class'),
    path('edit-dance-class/<int:id>/', edit_dance_class, name='edit-dance-class'),
    path('dance-class-detail/<int:id>', dance_class_detail, name='dance-class-detail')


]