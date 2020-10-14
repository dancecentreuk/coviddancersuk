from django.urls import path
from .views import inbox, new_conversation, communication_detail, outbox


app_name = 'mail'


urlpatterns = [
    # path('new_conversation', )
    path('inbox/', inbox, name='inbox'),
    path('outbox/', outbox, name='outbox'),
    path('message/new/', new_conversation, name='new-message'),
    path('message/communication/<pk>/', communication_detail, name='communication'),
]