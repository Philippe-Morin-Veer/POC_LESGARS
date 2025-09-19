import RPi.GPIO as GPIO
import dht11
import time
import paho.mqtt.client as mqtt

broker = '10.4.1.107'
port = 1883
topic = "temperature"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def main():
    # Initialisation du client MQTT
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()

    # Initialisation GPIO et capteur DHT11
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    instance = dht11.DHT11(pin=17)

    try:
        while True:
            result = instance.read()
            if result.is_valid():
                print(f"Temperature: {result.temperature:.1f} C")
                client.publish(topic, f"Temperature: {result.temperature} C",qos=1)
            else:
                print(f"Error: {result.error_code}")
            time.sleep(8)
    except KeyboardInterrupt:
        print("Arrêt par l'utilisateur.")
    except Exception as e:
        print(f"Erreur inattendue : {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        GPIO.cleanup()
        print("Nettoyage terminé.")

if __name__ == "__main__":
    main()