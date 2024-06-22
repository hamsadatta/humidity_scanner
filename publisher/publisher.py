import paho.mqtt.client as mqtt
import random
import time

class MQTTPublisher:
    def __init__(self, broker_address, broker_port, topic):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.topic = topic
        self.client = mqtt.Client()

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port)

    def publish(self):
        try:
            while True:
                # Generate a random humidity value
                humidity = random.uniform(30, 40)              
                self.client.publish(self.topic, f"Humidity: {humidity:.2f}%")
                print(f"Published: Humidity: {humidity:.2f}%")
                time.sleep(1)
        except KeyboardInterrupt:
            self.client.disconnect()
            print("Publisher disconnected.")

def main():
    publisher = MQTTPublisher(broker_address="broker.hivemq.com", broker_port=1883, topic="home/humidity17")
    publisher.connect()
    publisher.publish()

if __name__ == "__main__":
    main()
