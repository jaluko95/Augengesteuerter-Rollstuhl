import Eye_tracking as et
import Taster
from time import sleep
import multiprocessing as mp
from ctypes import c_bool
import Rover
import Poti
import RPi.GPIO as GPIO

try:        
    x = mp.Value('i', 0) # x koordinate der Pupille 
    taster_value = mp.Value(c_bool, False) #Ein/ Aus schalten der Motoren
    v = mp.Array('i', 2) # geschwindigkeit; index 0 = links/ index 1 = rechts
    brightness = mp.Value('i', 70)

    #initialisieren der Prozesse
    tracking = mp.Process(target=et.get_position, args=(x, brightness))
    taster = mp.Process(target=Taster.switch_OnOff, args=(taster_value,))
    rover = mp.Process(target=Rover.rover, args=(v,))
    poti = mp.Process(target=Poti.get_value, args=(brightness,))

    poti.start()
    tracking.start()
    taster.start()


    #Motoren mit v=0 starten
    v[0] = 0
    v[1] = 0
    rover.start()

    #"falsche" koordinaten mit maximalen x werten filtern
    #50 160 290
    #max wert rechts: 50
    #max wert links: 290

    while True:
        while taster_value.value == True: #sobald start/stop-knopf gedrückt wurde, fahre los:
            if(x.value > 0 and x.value > 50 and x.value < 290): #Wenn Position der Pupille erkannt wird
                if(x.value < 140):
                   #fahre nach rechts
                    v[0] = 50
                    v[1] = 25
                    #print("rechts")
                elif(x.value > 180):
                    # fahre nach links
                    v[0] = 25
                    v[1] = 50
                    #print("links")
                elif(x.value > 140 and x.value < 180):
                    #fahre geradeaus
                    v[0] = 50
                    v[1] = 50
                    print("gerade")
            else:#anhalten wenn Pupille nicht erkannt wird
                v[0] = 0
                v[1] = 0
        #anhalten wenn start/stop-knopf betätigt wird
        v[0] = 0
        v[1] = 0
except KeyboardInterrupt:
    print("Programm beenden..")
    poti.terminate()
    taster.terminate()
    tracking.terminate()
    rover.terminate()
    GPIO.cleanup()