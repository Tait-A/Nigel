import paho.mqtt.client as mqtt

# MQTT broker information
broker_address = "192.168.105.135"  # Assuming this is your local network device
broker_port = 1883  # Default MQTT port

# MQTT topic
topic = "test/topic"

# Message to be sent
message = "Hello, from DICE!"

# Callback function for on_connect event
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Once connected, publish the message
        client.publish(topic, message)
        print(f"Message '{message}' sent to topic '{topic}'")
    else:
        print("Failed to connect to MQTT Broker")

# Callback function for on_publish event
def on_publish(client, userdata, mid):
    print("Message published!")

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Assign on_connect and on_publish callback functions
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to MQTT broker
client.connect(broker_address, broker_port)

# Start the loop
client.loop_forever()
