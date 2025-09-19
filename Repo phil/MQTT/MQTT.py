import RPi.GPIO as GPIO
import dht11
import time 
import random
import paho.mqtt.client as mqtt

broker = '10.4.1.107'
port = 1883
topic = "temperature"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect(broker, port)

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 17
instance = dht11.DHT11(pin = 17)

client.loop_start()
while True:
    result = instance.read()
    if result.is_valid():
        print("Temperature: %-3.1f C" % result.temperature)
        result=client.publish(topic, "Temperature: %d C" % result.temperature)
    else:
        print("Error: %d" % result.error_code)
    time.sleep(8)
client.loop_stop()