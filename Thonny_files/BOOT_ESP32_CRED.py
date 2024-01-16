import os
from machine import Pin
import time
import CREDENCIALES as cred

from machine import SDCard
import network
from machine import I2S
from ftplib import FTP

def SDboot():
    miso_pin = Pin(19)
    mosi_pin = Pin(23)
    sck_pin = Pin(18)
    cs_pin = Pin(5)

    # Inicializar la tarjeta SD
    print("------------------------------------")
    print("Montando Tarjeta SD")
    sdcard = SDCard(slot=2, sck=sck_pin, miso=miso_pin, mosi=mosi_pin, cs=cs_pin, freq=5000)
    os.mount(sdcard, "/sd")
    print("Tarjeta SD montada con exito")
    print("------------------------------------")
    print("\n")
    return 0

def SetNetwork():
    ssid = cred.SSID
    password = cred.WIFIPASS

    # Create a station interface
    sta = network.WLAN(network.STA_IF)

    # Activate the station interface
    sta.active(True)

    # Connect to the Wi-Fi network
    print("------------------------------------")
    print("Estableciendo conexion Wifi")
    sta.connect(ssid, password)

    # Wait for the connection to be established
    while not sta.isconnected():
        time.sleep(1)

    print("Connected to Wi-Fi network")

    # Get the IP address of the ESP32
    ip_address = sta.ifconfig()[0]
    print("IP address:", ip_address)
    print("------------------------------------")
    print("\n")
    
    return 0

def create_wav_header(sampleRate, bitsPerSample, num_channels, num_samples):
    datasize = num_samples * num_channels * bitsPerSample // 8
    o = bytes("RIFF", "ascii")  # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(
        4, "little"
    )  # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE", "ascii")  # (4byte) File type
    o += bytes("fmt ", "ascii")  # (4byte) Format Chunk Marker
    o += (16).to_bytes(4, "little")  # (4byte) Length of above format data
    o += (1).to_bytes(2, "little")  # (2byte) Format type (1 - PCM)
    o += (num_channels).to_bytes(2, "little")  # (2byte)
    o += (sampleRate).to_bytes(4, "little")  # (4byte)
    o += (sampleRate * num_channels * bitsPerSample // 8).to_bytes(4, "little")  # (4byte)
    o += (num_channels * bitsPerSample // 8).to_bytes(2, "little")  # (2byte)
    o += (bitsPerSample).to_bytes(2, "little")  # (2byte)
    o += bytes("data", "ascii")  # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4, "little")  # (4byte) Data size in bytes
    return o

def MicI2S():
    print("------------------------------------")
    print("Definiendo objeto de microfono I2S y configuracion de audio")
    # ======= I2S CONFIGURATION =======
    SCK_PIN = 26
    WS_PIN = 22
    SD_PIN = 21
    I2S_ID = 0
    BUFFER_LENGTH_IN_BYTES = 40000
    # ======= I2S CONFIGURATION =======
    
    # ======= AUDIO CONFIGURATION =======
    RECORD_TIME_IN_SECONDS = 5
    WAV_SAMPLE_SIZE_IN_BITS = 16
    FORMAT = I2S.MONO
    SAMPLE_RATE_IN_HZ = 16000
    # ======= AUDIO CONFIGURATION =======
    
    format_to_channels = {I2S.MONO: 1, I2S.STEREO: 2}
    NUM_CHANNELS = format_to_channels[FORMAT]
    WAV_SAMPLE_SIZE_IN_BYTES = WAV_SAMPLE_SIZE_IN_BITS // 8
    RECORDING_SIZE_IN_BYTES = (
        RECORD_TIME_IN_SECONDS * SAMPLE_RATE_IN_HZ * WAV_SAMPLE_SIZE_IN_BYTES * NUM_CHANNELS
    )

    # create header for WAV file and write to SD card
    wav_header = create_wav_header(
        SAMPLE_RATE_IN_HZ,
        WAV_SAMPLE_SIZE_IN_BITS,
        NUM_CHANNELS,
        SAMPLE_RATE_IN_HZ * RECORD_TIME_IN_SECONDS,
    )
    
    audio_in = I2S(
    I2S_ID,
    sck=Pin(SCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.RX,
    bits=WAV_SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=BUFFER_LENGTH_IN_BYTES,
    )
    
    print("Creacion exitosa")
    print("------------------------------------")
    print("\n")
    
    return audio_in, wav_header, RECORDING_SIZE_IN_BYTES

def Conexion_FTP():
    # Connect to the FTP server
    print("------------------------------------")
    print("Estableciendo conexion a servidor FTP")
    ftp = FTP(cred.SERVER, 21, cred.USER, cred.USERPASS)
    ftp.pwd()
    ftp.retrlines('LIST')
    print("Conexion establecida")
    print("------------------------------------")
    print("\n")

    return ftp








