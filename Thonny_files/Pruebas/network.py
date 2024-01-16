import network
import time

# Define the Wi-Fi network details
ssid = "VTR-0099193"
password = "ddXsgqzS5gvw"

# Create a station interface
sta = network.WLAN(network.STA_IF)

# Activate the station interface
sta.active(True)

# Connect to the Wi-Fi network
sta.connect(ssid, password)

# Wait for the connection to be established
while not sta.isconnected():
    time.sleep(1)

print("Connected to Wi-Fi network")

# Get the IP address of the ESP32
ip_address = sta.ifconfig()[0]
print("IP address:", ip_address)