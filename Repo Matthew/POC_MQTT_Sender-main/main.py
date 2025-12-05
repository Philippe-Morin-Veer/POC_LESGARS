import RPi.GPIO as GPIO
import dht11
import time
import paho.mqtt.client as mqtt

broker_address = "10.4.1.180"  
topic = "sensor/temperature"
topic2 = "sensor/humidity"
client = mqtt.Client()
client.connect(broker_address)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin=17)

while True:
    result = instance.read()
    if result.is_valid():
        print("Temperature: %-3.1f C" % result.temperature)
        print("Humidity: %-3.1f %%" % result.humidity)
        client.publish(topic, result.temperature, qos = 1)
        client.publish(topic2, result.humidity, qos = 1)
    else:
        print("Error: %d" % result.error_code)
    time.sleep(2)