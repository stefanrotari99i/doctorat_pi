from django.urls import path
from . import views

urlpatterns = [
    path('sensor/', views.sensor_data, name='sensor_data'),
    path('download-sensor-data/', views.download_sensor_data, name='download_sensor_data'),
]
