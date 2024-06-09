import serial.tools.list_ports

import sys

import time

import random
import json
from Adafruit_IO import MQTTClient

#from simple_ai import image_detector

#from port import *

from rs485 import *

#from adafruit import *

class Adafruit_MQTT:
    # AIO_FEED_IDs = ["cambien1", "cambien2"]
    # AIO_USERNAME = "robotanh"
    # AIO_KEY = ""
    AIO_FEED_IDs = [
    "mixer1", 
    "mixer2", 
    "mixer3",
    "next-cycle",
    "selector", 
    "pump-in", 
    "pump-out",
    "active"
]
    AIO_USERNAME = "dinhvan2211"
    AIO_KEY = ""
    recvCallBack = None

    def connected(self, client):
        print("Connected ...")
        for feed in self.AIO_FEED_IDs:
            client.subscribe(feed)

    def subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed...")

    def disconnected(self, client):
        print("Disconnected... Trying to reconnect.")
        self.client.reconnect()
    def message(self, client, feed_id, payload):
        try:
            # Check if payload is a JSON string
            if payload.startswith("{") and payload.endswith("}"):
                data = json.loads(payload)
                if self.recvCallBack:
                    self.recvCallBack(feed_id, data)
            elif payload.isdigit():
                # Handle payload if it's an integer
                value = int(payload)
                if self.recvCallBack:
                    self.recvCallBack(feed_id, value)
            else:
                # Handle other types of payload (e.g., "1/1915")
                # Here you can implement custom logic to parse this type of payload
                # For example, splitting the string and extracting relevant data
                parts = payload.split("/")
                if len(parts) == 2:
                    # Assuming parts[0] is cycles and parts[1] is time_start
                    cycles = int(parts[0])
                    time_start = parts[1]
                    # Use the extracted data as needed
                    if self.recvCallBack:
                        self.recvCallBack(feed_id, {"cycles": cycles, "time-start": time_start})
                else:
                    print(f"Unexpected payload format: {payload}")
        except Exception as e:
            print(f"Error processing payload: {e}")


    def setRecvCallBack(self, func):
        self.recvCallBack = func

    def __init__(self):
        self.client = MQTTClient(self.AIO_USERNAME, self.AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()
