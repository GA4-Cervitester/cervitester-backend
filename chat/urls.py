from django.urls import path

from .views import MessagesView, AddMessageView
urlpatterns = [
    path('get-messages/', MessagesView),
    path('add-message/', AddMessageView)
]
