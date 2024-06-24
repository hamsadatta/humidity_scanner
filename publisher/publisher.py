import paho.mqtt.client as mqtt
import random
import time
import yaml

class MQTTPublisher:
    def __init__(self, config):
        self.broker_address = config['mqtt']['broker_address']
        self.broker_port = config['mqtt']['broker_port']
        self.topic = config['mqtt']['topic']
        try:
            self.client = mqtt.Client()
        except Exception as e:
            print(f"Failed to create MQTT client: {e}")

    def connect(self):
        try:
            self.client.connect(self.broker_address, self.broker_port)
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")

    def publish(self):
        try:
            while True:
                # Generate a random humidity value
                humidity = random.uniform(55, 57)
                try:
                    self.client.publish(self.topic, f"Humidity: {humidity:.2f}%")
                    print(f"Published: Humidity: {humidity:.2f}%")
                except Exception as e:
                    print(f"Failed to publish message: {e}")
                time.sleep(1)
        except KeyboardInterrupt:
            try:
                self.client.disconnect()
                print("Publisher disconnected.")
            except Exception as e:
                print(f"Failed to disconnect from MQTT broker: {e}")

def main():
    with open("./../config.yaml", "r") as f:
        config = yaml.safe_load(f)

    publisher = MQTTPublisher(config)
    publisher.connect()
    publisher.publish()

if __name__ == "__main__":
    main()
