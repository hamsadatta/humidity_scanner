import paho.mqtt.client as mqtt
import requests
import json
import time
import yaml
import os
from data_storage import DataStorage

class MQTTSubscriber:
    def __init__(self, config):
        self.mqtt_broker_address = config['mqtt']['broker_address']
        self.mqtt_broker_port = config['mqtt']['broker_port']
        self.mqtt_topic = config['mqtt']['topic']
        self.tb_broker_address = config['thingsboard']['broker_address']
        self.tb_broker_port = config['thingsboard']['broker_port']
        self.access_token = config['thingsboard']['access_token']
        self.telemetry_topic = config['thingsboard']['telemetry_topic']

        try:
            self.is_system_online()
            self.mqtt_client = mqtt.Client(client_id="subscriber_client", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
        except Exception as e:
            print(f"Failed to create MQTT client: {e}")

        try:
            self.is_system_online()
            self.tb_client = mqtt.Client(client_id="thingsboard_client", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
            self.tb_client.username_pw_set(self.access_token)
        except Exception as e:
            print(f"Failed to create ThingsBoard client: {e}")

        self.connected = False

        self.data_storage = DataStorage()

        self.tb_client.on_connect = self.on_tb_connect
        self.tb_client.on_disconnect = self.on_tb_disconnect

    def on_message(self, client, userdata, message):
        print(f"Received message: {message.payload.decode()} on topic {message.topic}")
        humidity_value = float(message.payload.decode().split(':')[1].strip(' %'))
        self.data_storage.store_data(humidity_value)
        self.send_data(humidity_value)

    def on_connect(self, client, userdata, flags, reason_code, properties=None):
        print(f"Connected with reason code {reason_code}")
        client.subscribe(self.mqtt_topic)

    def on_tb_connect(self, client, userdata, flags, reason_code, properties=None):
        print(f"Connected to ThingsBoard with reason code {reason_code}")
        self.connected = True
        self.send_stored_data()

    def on_tb_disconnect(self, client, userdata, rc):
        print(f"Disconnected from ThingsBoard with reason code {rc}")
        self.connected = False

    def connect(self):
        try:
            self.mqtt_client.on_connect = self.on_connect
            self.mqtt_client.on_message = self.on_message
            self.mqtt_client.connect(self.mqtt_broker_address, self.mqtt_broker_port)
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")

        try:
            self.tb_client.connect(self.tb_broker_address, self.tb_broker_port, keepalive=60)
        except Exception as e:
            print(f"Failed to connect to ThingsBoard: {e}")

    def subscribe(self):
        try:
            self.mqtt_client.loop_start()
            self.tb_client.loop_start()
        except Exception as e:
            print(f"Error in MQTT loop: {e}")

    def send_data(self, humidity_value):
        try:
            if self.is_system_online():
                payload = {
                    "Humidity": humidity_value
                }
                result = self.tb_client.publish(self.telemetry_topic, json.dumps(payload))
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print(f"Successfully sent data to ThingsBoard: {humidity_value}")
                else:
                    print(f"Failed to send data to ThingsBoard: {result}")
            else:
                print(f"Storing data locally as connection to ThingsBoard is unavailable.")
        except Exception as e:
            print(f"Error while sending data to ThingsBoard: {e}")

    def send_stored_data(self):
        if not self.is_system_online():
            return

        rows = self.data_storage.get_stored_data()
        for row in rows:
            timestamp, humidity_value = row
            try:
                payload = {
                    "Humidity": humidity_value
                }
                result = self.tb_client.publish(self.telemetry_topic, json.dumps(payload))
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print(f"Successfully sent stored data to ThingsBoard: {humidity_value}")
                    self.data_storage.delete_data(timestamp)
                else:
                    print(f"Failed to send stored data to ThingsBoard: {result}")
            except Exception as e:
                print(f"Error while sending stored data to ThingsBoard: {e}")

    def is_system_online(self):
        try:
            response = requests.get("https://www.google.com", timeout=5)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Internet connection check failed: {e}")
            return False

def main():
    with open("./../config.yaml", "r") as f:
        config = yaml.safe_load(f)

    subscriber = MQTTSubscriber(config)
    subscriber.connect()
    subscriber.subscribe()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
