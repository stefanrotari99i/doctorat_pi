import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from sensor_project.hx711_sensor import HX711  # Assuming the HX711 class is in hx711_sensor.py
from datetime import datetime
# from sensor_app.models import SensorData, SensorSession

class SensorConsumer(AsyncWebsocketConsumer):
    start_time = None

    async def connect(self):
        await self.accept()

        # Initialize the HX711 sensor

        self.hx = HX711(dout_pin=5, pd_sck_pin=6)


       # Retrieve or create the current session's start time
        session = await self.get_or_create_session()
        self.start_time = session.start_time

        # Start sending sensor data in real-time
        self.reading_task = asyncio.create_task(self.send_sensor_data())

    async def disconnect(self, close_code):
        self.hx.clean_and_exit()
        if self.reading_task:
            self.reading_task.cancel()


    async def send_sensor_data(self):
        try:
            while True:
                try:
                    # Attempt to read the sensor value
                    value = self.hx.read()

                    if not value:
                        print(f"Sensor error: {e}")
                        value = None
                        status = "Inactive"
                    else:
                        status = "Active"
                        formatted_start_time = self.start_time.strftime("%Y-%m-%d %H:%M:%S")

                except Exception as e:
                    print(f"Sensor error: {e}")
                    value = None
                    status = "Inactive"
                    # If reading fails, set status to "Inactive"

                # await self.save_sensor_data(value)
                # Send the value over WebSocket
                await self.send(text_data=json.dumps({
                    "value": value,
                    "start_time": formatted_start_time,
                    "status": status
                }))

                # Delay between readings
                await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Error: {e}")
        except asyncio.CancelledError:
            print("Task cancelled.")


    async def get_or_create_session(self):
        from sensor_app.models import SensorSession  # Import here to avoid registry issues
        from asgiref.sync import sync_to_async

        # Retrieve the latest session or create a new one
        session = await sync_to_async(SensorSession.objects.last)()
        if not session:
            session = await sync_to_async(SensorSession.objects.create)()
        return session

    def reset_session():
        SensorSession.objects.create()

    # def save_sensor_data(self, value):
    #     SensorData.objects.create(value=value)


