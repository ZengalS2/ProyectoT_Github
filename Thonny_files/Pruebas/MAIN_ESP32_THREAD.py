import boot as bt
import time as tm
import ntptime
from _thread import start_new_thread

def loopRecord():
    while True:
        audio_in, wav_header, RECORDING_SIZE_IN_BYTES = bt.MicI2S()
        print("	OK HASTA EL LLAMADO")
        
        tiempo = tm.localtime()
        audio_name = 'mic_'+str(tiempo[0])+str("%02d" % tiempo[1])+str("%02d" % tiempo[2])+'_'+str("%02d" % tiempo[3])+'_'+str("%02d" % tiempo[4])+'_'+str("%02d" % tiempo[5])+'.wav'
        
        wav = open("/sd/{}".format(audio_name), "wb")
        num_bytes_written = wav.write(wav_header)

        # allocate sample arrays
        # memoryview used to reduce heap allocation in while loop
        mic_samples = bytearray(10000)
        mic_samples_mv = memoryview(mic_samples)

        num_sample_bytes_written_to_wav = 0

        print("Recording size: {} bytes".format(RECORDING_SIZE_IN_BYTES))
        print("==========  START RECORDING ==========")
        try:
            while num_sample_bytes_written_to_wav < RECORDING_SIZE_IN_BYTES:
                # read a block of samples from the I2S microphone
                num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)
                if num_bytes_read_from_mic > 0:
                    num_bytes_to_write = min(
                        num_bytes_read_from_mic, RECORDING_SIZE_IN_BYTES - num_sample_bytes_written_to_wav
                    )
                    # write samples to WAV file
                    num_bytes_written = wav.write(mic_samples_mv[:num_bytes_to_write])
                    num_sample_bytes_written_to_wav += num_bytes_written

            print("==========  DONE RECORDING ==========")
        except (KeyboardInterrupt, Exception) as e:
            print("caught exception {} {}".format(type(e).__name__, e))

        # cleanup
        wav.close()
        try:
            print("SD card storage:{}".format(os.listdir("/sd")))
        except:
            print("Error al acceder a la tarjeta sd")
        #os.umount("/sd")
        #sd.deinit()
        audio_in.deinit()
        
        print("-----------------------------------------------------")
        print("\n")
        
        time.sleep(2)
    return 0

def loopUpload(ftp):
    while True:
        files = ftp.nlst()
        num = len(files) 
        
        files = [f for f in os.listdir("/sd")]
        filesOK = files[1:] #ignora el archivo System Volume de la sd
        
        if len(filesOK) == 0:
            print("-----------------------------------------------------")
            print("Sin archivos que subir, esperando...")
            print("-----------------------------------------------------")
            time.sleep(2)
            continue
        
        print("Numero de audios guardados en este punto en el servidor: "+ str(num))
        if num >= 300:
            print("Servidor a capacidad maxima establecida, esperando")
            time.sleep(5)
        else:
            while os.stat("/sd/{}".format(filesOK[0]))[6] != 160044:
                time.sleep_ms(500)
            time.sleep_ms(100)
            # Upload a file
            print("-----------------------------------------------------")
            print("Cargando audio a servidor")
            try:
                with open("/sd/{}".format(filesOK[0]), 'rb') as f:
                    print(f)
                    ftp.storbinary('STOR '+filesOK[0], f)
                os.remove("/sd/{}".format(filesOK[0]))
                
                print("Audio cargado con exito")
                print("-----------------------------------------------------")
            except:
                print("Error en la carga del archivo")
                print("-----------------------------------------------------")
        
    return 0

def main():
    
    bt.SDboot()
    bt.SetNetwork()
    ftp = bt.Conexion_FTP()
    ftp.cwd("audios")
    
    ntptime.settime()     #Set del reloj interno de tiempo al tiempo actual
    
    start_new_thread(loopRecord, ())
    loopUpload(ftp)
    
    return 0