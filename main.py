import paho.mqtt.client as mqtt
import boto3
import json
from botocore.exceptions import ClientError

MQTT_SERVER = "192.168.0.10"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe('parking/status')

def on_publish(client, userdata, result):
    print("data published")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    msg.payload = json.loads(msg.payload)

    print('Message Topic: ', msg.topic)
    print('Payload: ', msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)
client.loop_forever()