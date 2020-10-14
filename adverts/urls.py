from django.urls import path
from .views import adverts, advert_detail, advert_create, edit_job, delete_advert, postings, \
    posting_create, edit_posting, posting_detail, delete_posting, search, postings_search



urlpatterns = [

    path('', adverts, name='adverts'),
    path('advert/<pk>/<slug>/', advert_detail, name='advert-detail'),
    path('create/', advert_create, name = 'create-advert'),
    path('edit/<pk>/<slug>/', edit_job, name='edit-advert'),
    path('delete/<pk>/<slug>/', delete_advert, name='delete-advert-button'),
    path('postings/', postings, name='postings'),
    path('create/posting/', posting_create, name='create-posting'),
    path('posting/edit/<pk>/<slug>/', edit_posting, name='edit-posting'),
    path('new-posting/<pk>/<slug>/', posting_detail, name='posting-detail'),
    path('delete/posting/<pk>/<slug>/', delete_posting, name='delete-posting-button'),
    path('search/adverts/', search, name='search'),
    path('search/postings/', postings_search, name='search-postings')

]