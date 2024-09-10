from django.urls import path
from chat.views import *

app_name = 'chat'  

urlpatterns = [
    path('', chat, name='chat'),
    path('send-question/', send_question, name='send-question'),
]