from adafruit import Adafruit_MQTT
from timer import *
import threading
import fsm
import time
import random
from rs485 import *
import json

state = {
    "next-cycle": 1,
    "mixer1": 2,
    "mixer2": 2,
    "mixer3": 2,
    "selector": None,
    "pump-in": 2,
    "pump-out": 2,
    "time-start": "20:23",
    "active": 1,
}

sched_active = [{
    "next-cycle": 1,
    "mixer1": 2,
    "mixer2": 2,
    "mixer3": 2,
    "selector": None,
    "pump-in": 2,
    "pump-out": 2,
    "time-start": "19:30",
    "active": 1,
},
               {
    "next-cycle": 1,
    "mixer1": 2,
    "mixer2": 2,
    "mixer3": 2,
    "selector": None,
    "pump-in": 2,
    "pump-out": 2,
    "time-start": "11:23",
    "active": 1,
}
               {
    "next-cycle": 1,
    "mixer1": 2,
    "mixer2": 2,
    "mixer3": 2,
    "selector": None,
    "pump-in": 2,
    "pump-out": 2,
    "time-start": "11:23",
    "active": 1,
}]

def data_callback(feed_id, payload):
    key = feed_id
    print("Received payload:", payload)
    
    try:
        if isinstance(payload, dict):
            new_schedule = json.loads(payload)
            
            required_keys = {"next-cycle", "mixer1", "mixer2", "mixer3", "selector", "pump-in", "pump-out", "time-start", "active"}
            if required_keys.issubset(new_schedule.keys()):
                time_start = new_schedule["time-start"]
                if len(time_start) == 4:
                    new_schedule["time-start"] = f"{time_start[:2]}:{time_start[2:]}"
                
                # Thêm lịch trình mới vào FarmScheduler
                scheduler.add_schedule(new_schedule)
                print("New schedule added:", new_schedule)
            else:
                print("Invalid schedule format:", new_schedule)
        elif key in state:
            state[key] = payload
            print(f"Updated {key} to {state[key]}")
        else:
            print(f"No handler found for feed: {feed_id}")
    except Exception as e:
        print(f"Error processing payload: {e}")



def main_loop():
    start_sched = fsm.FarmScheduler()
    while True:
        print(state)
        if state["active"] == 1:
            sched_active.append(state.copy())
            print("Activated new schedule!")
            print(state)
            state["active"] = 0  # Reset the active flag

        for schedule in sched_active:
            start_sched.add_schedule(schedule)
            start_sched.run()
            sched_active.remove(schedule)

        time.sleep(1)

def publish_data(client):
    sensor = Physic()
    while True:
        # Publish random data to a feed
        feed_id1 = "assignment.temperature"  # Example feed ID
        feed_id2 = "assignment.humidity"
        value1 = sensor.readSensors("soil_temperature")/100  # Example temperature value
        value2 = sensor.readSensors("soil_moisture")/100 
        client.publish(feed_id1, value1)
        client.publish(feed_id2, value2)
        # client.publish(feed_id1, readTemperature())
        # client.publish(feed_id2, readMoisture())
        print(f"Published {value1} to {feed_id1}")
        print(f"Published {value2} to {feed_id2}")
        time.sleep(5)  # Wait for 5 seconds before publishing next data

# Initialize the Adafruit MQTT client and set the callback
adafruit_client = Adafruit_MQTT()
adafruit_client.setRecvCallBack(data_callback)

# Create threads for MQTT client and main loop
main_loop_thread = threading.Thread(target=main_loop)
publish_thread = threading.Thread(target=publish_data, args=(adafruit_client.client,))
# Start the threads
main_loop_thread.start()
publish_thread.start()
# Join the threads to the main thread
main_loop_thread.join()
publish_thread.join()
