import paho.mqtt.client as mqtt
import ssl
import time
import requests

# 🔹 AWS CONFIG
ENDPOINT = "YOUR_ENDPOINT_HERE"
CLIENT_ID = "axon_device"
TOPIC = "axon/data"

# 🔹 BLYNK CONFIG
BLYNK_TOKEN = "YOUR_BLYNK_TOKEN"

# 🔹 Function to send data to Blynk
def send_to_blynk(value):
    url = f"https://blynk.cloud/external/api/update?token={BLYNK_TOKEN}&V0={value}"
    try:
        requests.get(url)
    except:
        print("Blynk error")

# 🔹 AWS Connection callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to AWS IoT")
    else:
        print("❌ Connection failed")

# 🔹 MQTT setup
client = mqtt.Client(CLIENT_ID)
client.on_connect = on_connect

client.tls_set(
    ca_certs="AmazonRootCA1.pem",
    certfile="device.pem.crt",
    keyfile="private.pem.key",
    tls_version=ssl.PROTOCOL_TLSv1_2
)

# 🔹 Connect to AWS
client.connect(ENDPOINT, 8883)
client.loop_start()

# 🔁 MAIN LOOP
while True:
    message = "Robot running"

    # Send to AWS
    client.publish(TOPIC, message)
    print("📤 Sent to AWS:", message)

    # Send to Blynk
    send_to_blynk(1)

    time.sleep(2)