from django.urls import path
from .views import operationPage, resultsPage

app_name = 'operation'
urlpatterns = [
    path('operation/', operationPage, name='operationPage'),
    path('operation/results/<int:city>', resultsPage, name='resultsPage'),
]