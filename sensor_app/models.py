from django.db import models

class SensorSession(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session started at {self.start_time}"

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically add current timestamp
    value = models.FloatField()  # Sensor value

    def __str__(self):
        return f"{self.timestamp}: {self.value}"
