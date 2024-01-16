from machine import SDCard
from machine import Pin
from machine import I2S
import os
import wave
import time

miso_pin = Pin(19)
mosi_pin = Pin(23)
sck_pin = Pin(18)
cs_pin = Pin(5)

# Inicializar la tarjeta SD
sdcard = SDCard(slot=2,
                sck=sck_pin,
                miso=miso_pin,
                mosi=mosi_pin,
                cs=cs_pin, f
                req=5000)
os.mount(sdcard, "/sd")


mic_ck_pin = Pin(26)
mic_ws_pin = Pin(22)
mic_da_pin = Pin(21)

audio_in = I2S(
    0,
    sck=mic_ck_pin,
    ws=mic_ws_pin,
    sd=mic_da_pin,
    mode=I2S.RX,
    bits=16,
    format=I2S.MONO,
    rate=16000,
    ibuf=10000
)

sample_rate = 16000
sample_width_bytes = 2
channels = 1
segundos = 3

buffer = bytearray(sample_rate * sample_width_bytes * channels * segundos) #archivo sin procesar 
audio_in.readinto(buffer)

with wave.open('/sd/audio.wav', 'wb') as f:  
   f.setnchannels(channels)
   f.setsampwidth(sample_width_bytes)
   f.setframerate(sample_rate)
   f.writeframesraw(buffer)
   
