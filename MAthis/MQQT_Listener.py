import paho.mqtt.client as mqtt

client_id = "10.4.1.107"

def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")

def on_message(client, userdata, message):
    # userdata is the structure we choose to provide, here it's a list()
    print (f"Received message '{message.payload.decode()}'")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe("temperature", qos=1)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id = client_id, clean_session = False)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe


mqttc.user_data_set([])
mqttc.connect("10.4.1.107", 1883)
mqttc.loop_forever()
print(f"Received the following message: {mqttc.user_data_get()}")