from django.urls import path
from .views import venues, add_venue, venue_detail, edit_venue, delete_venue, venue_search


urlpatterns = [

    path('venues-list/', venues, name='venues'),
    path('add-venue/', add_venue, name='add-venue'),
    path('venue-detail/<int:pk>/<slug:slug>/', venue_detail, name='venue-detail'),
    path('venue-edit/<int:pk>/<slug:slug>/', edit_venue, name='edit-venue'),
    path('venue-delete/<int:pk>/<slug:slug>/', delete_venue, name='delete-venue'),
    path('search/venue/', venue_search, name='search-venue'),

]