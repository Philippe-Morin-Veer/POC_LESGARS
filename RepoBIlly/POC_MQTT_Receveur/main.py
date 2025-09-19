import paho.mqtt.client as mqtt

broker_address = "10.4.1.180"
topicTemp = "sensor/temperature"
topicHum = "sensor/humidity"
client_id = "ReceveurTempHum"  # Un identifiant unique

def on_connect(client, userdata, flags, rc):
    client.subscribe(topicTemp, qos=1) 
    client.subscribe(topicHum, qos=1) 

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

client = mqtt.Client(client_id=client_id, clean_session=False)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address)
client.loop_forever()