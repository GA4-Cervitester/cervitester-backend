from django.urls import path

from admin.views import RegisterView, GetDataView, DisableUserView, VerifyDoctor, EnableUserView,AddModelView,SetActiveModelView


urlpatterns = [
    path('register', RegisterView),
    path('get-data', GetDataView),
    path('verify-doctor', VerifyDoctor),
    path('disable-user', DisableUserView),
    path('enable-user', EnableUserView),
    path('add-model', AddModelView),
    path('set-active-model', SetActiveModelView),
]
