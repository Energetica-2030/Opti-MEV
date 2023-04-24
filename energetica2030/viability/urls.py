from django.urls import path
from .views import viabilityPage, getVehicleData

app_name = 'viability'
urlpatterns = [
    path('viability/', viabilityPage, name='viabilityPage'),
    path('viability/getVehicleData/<str:name>', getVehicleData, name='getVehicleData')
]