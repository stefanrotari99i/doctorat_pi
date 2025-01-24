from django.shortcuts import render
import csv
from django.http import HttpResponse
from .models import SensorData

# Create your views here.
def sensor_data(request):
    return render(request, "sensor_app/index.html",)

def download_sensor_data(request):
    # Create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sensor_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'Value'])

    # Fetch all sensor data from the database
    for data in SensorData.objects.all():
        writer.writerow([data.timestamp, data.value])

    return response
