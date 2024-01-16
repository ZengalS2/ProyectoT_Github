from ftplib import FTP

"""
class DebugFTP(FTP):
    debugging = 1

ftp = DebugFTP(host='ftp-serveralways.alwaysdata.net',
               port=21,
               user='serveralways_esp32',
               passwd='Always322981')
"""

# Connect to the FTP server
ftp = FTP('ftp-serveralways.alwaysdata.net', 21, 'serveralways_esp32', 'Always322981')
ftp.pwd()
#ftp.retrlines('LIST')
#print("Conexion establecida")


files = ftp.retrlines('LIST')
num = 0
for line in files:
    num = num+1
print(int(num/7))
  
"""
# Upload a file
print("-----------------------------------------------------")
print("Cargando audio a servidor")
ftp.cwd("audios")
try:
    with open('/sd/mic.wav', 'rb') as f:
        print(f)
        ftp.storbinary('STOR mic_up.wav', f)
    print("Audio cargado con exito")
except:
    print("Error en la carga del archivo")
"""   

# Close the FTP connection
ftp.quit()

