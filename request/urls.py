from django.urls import path

from .views import AddRequestView, GetRequestByIdView, GetRequestsView, UpdateRequestView,RespondRequestView

urlpatterns = [
    path('add-request/', AddRequestView),
    path('get-request/', GetRequestsView),
    path('respond-request/',RespondRequestView),
    path('update-request/', UpdateRequestView),
]
