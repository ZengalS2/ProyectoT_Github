from machine import SDCard
from machine import Pin

miso_pin = Pin(19)
mosi_pin = Pin(23)
sck_pin = Pin(18)
cs_pin = Pin(5)

# Inicializar la tarjeta SD
sdcard = SDCard(slot=2, sck=sck_pin, miso=miso_pin, mosi=mosi_pin, cs=cs_pin, freq=5000)
os.mount(sdcard, "/sd")