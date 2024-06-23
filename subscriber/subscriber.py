import paho.mqtt.client as mqtt
import requests
import json
import time
from datetime import datetime

ACCESS_TOKEN = 'ADD_YOUR_TOKEN'  # Replace with your ThingsBoard device token
broker = "demo.thingsboard.io"  
port = 1883  
thingsboard_topic = "v1/devices/me/telemetry"  # ThingsBoard telemetry topic

class MQTTSubscriber:
    def __init__(self, mqtt_broker_address, mqtt_broker_port, mqtt_topic):
        self.mqtt_broker_address = mqtt_broker_address
        self.mqtt_broker_port = mqtt_broker_port
        self.mqtt_topic = mqtt_topic
        self.mqtt_client = mqtt.Client(client_id="subscriber_client", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
        self.tb_client = mqtt.Client(client_id="thingsboard_client", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
        self.tb_client.username_pw_set(ACCESS_TOKEN)
        self.tb_client.connect(broker, port, keepalive=60)

    def on_message(self, client, userdata, message):
        print(f"Received message: {message.payload.decode()} on topic {message.topic}")
        humidity_value = float(message.payload.decode().split(':')[1].strip(' %'))
        self.send_to_thingsboard(humidity_value)

    def on_connect(self, client, userdata, flags, reason_code, properties=None):
        print(f"Connected with reason code {reason_code}")
        client.subscribe(self.mqtt_topic)

    def connect(self):
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(self.mqtt_broker_address, self.mqtt_broker_port)

    def subscribe(self):
        self.mqtt_client.loop_start()

    def send_to_thingsboard(self, humidity_value):
        payload = {
            "Humidity": humidity_value
        }
        result = self.tb_client.publish(thingsboard_topic, json.dumps(payload))
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Successfully sent data to ThingsBoard: {humidity_value}")
        else:
            print(f"Failed to send data to ThingsBoard: {result}")

def main():
    mqtt_broker_address = "broker.hivemq.com"
    mqtt_broker_port = 1883
    mqtt_topic = "home/humidity17"

    subscriber = MQTTSubscriber(mqtt_broker_address, mqtt_broker_port, mqtt_topic)
    subscriber.connect()
    subscriber.subscribe()

    while True:
        time.sleep(1) 

if __name__ == "__main__":
    main()
