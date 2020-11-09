from django.urls import path
from .views import dance_classes, add_dance_class, edit_dance_class, dance_class_detail, delete_dance_class, \
    add_dance_class_review, dance_classes_search


urlpatterns = [


    path('courses/',  dance_classes, name='dance-classes'),
    path('add-dance-class/', add_dance_class, name='add-dance-class'),
    path('edit-dance-class/<int:id>/', edit_dance_class, name='edit-dance-class'),
    path('dance-class-detail/<int:id>/', dance_class_detail, name='dance-class-detail'),
    path('delete-dance-class/<int:pk>/', delete_dance_class, name='delete-dance-class'),
    path('search/dance-classes/', dance_classes_search, name='search-dance-classes'),


    path('add-dance-class-review/<int:id>/', add_dance_class_review, name='add-dance-class-review')


]