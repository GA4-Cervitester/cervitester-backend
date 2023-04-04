from django.urls import path

from authentication.views import ProfileInfoView, RegisterView, getPatient, getToken, getDoctors

urlpatterns = [
    path('register/<type>', RegisterView),
    path('get-token', getToken),
    path('get-profile', ProfileInfoView),
    path('get-patient', getPatient),
    path('get-doctors', getDoctors)
]
