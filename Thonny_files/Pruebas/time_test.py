import time as tm

tiempo = tm.localtime()
audio_name = 'mic_'+str(tiempo[0])+str("%02d" % tiempo[1])+str("%02d" % tiempo[2])+'_'+str("%02d" % tiempo[3])+'_'+str("%02d" % tiempo[4])+'_'+str("%02d" % tiempo[5])+'.wav'
print(audio_name)
