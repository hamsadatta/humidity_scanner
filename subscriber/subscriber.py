import paho.mqtt.client as mqtt

class MQTTSubscriber:
    def __init__(self, broker_address, broker_port, topic):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.topic = topic
        self.client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

    def on_message(self, client, userdata, message):
        print(f"Received message: {message.payload.decode()} on topic {message.topic}")

    def on_connect(self, client, userdata, flags, reason_code, properties=None):
        print(f"Connected with reason code {reason_code}")
        client.subscribe(self.topic)

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address, self.broker_port)

    def subscribe(self):
        self.client.loop_forever()

def main():
    subscriber = MQTTSubscriber(broker_address="broker.hivemq.com", broker_port=1883, topic="home/humidity17")
    subscriber.connect()
    subscriber.subscribe()

if __name__ == "__main__":
    main()
