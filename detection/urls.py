from django.urls import path

from .views import FileUploadView, OperatorView, RecordsView, AnnotationView

urlpatterns = [
    path('file/', FileUploadView),
    path('operate/', OperatorView),
    path('records/', RecordsView),
    path('annotate/', AnnotationView)
]
