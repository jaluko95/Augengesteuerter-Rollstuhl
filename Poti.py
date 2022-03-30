import spidev
from time import sleep
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(18, gpio.OUT)
gpio.output(18, gpio.HIGH) #stromversorgung des Potis

spi = spidev.SpiDev()      # SPI-Bus initialisieren
spi.open(0,0)              # SPI Bus 0, Client 0 oeffnen
spi.max_speed_hz=1000000   # Max. Geschw. begrenzen fuer stabiles Auslesen

def readMCP3008(channel):# auslesen des Signals auf entsprechendem Channel
  adc=spi.xfer2([1,(8+channel)<<4,0])
  wert = ((adc[1]&3) << 8) + adc[2]
  return wert

def get_value(value):
    while True: #frage zweimal pro Sekunde den Wert des Reglers ab
        v=readMCP3008(0) # A/D Wandler auf Channel 0 auslesen; v entspricht einer Zahl zwischen 0 und 1023
        p = int((v/10.23)/5 + 60)# umrechnen in Prozent (v/1023/100) und umrechnung in Helligkeitswert zwischen 60 und 80
        value.value = p #Helligkeitswert an Steuerung übergeben
        sleep (0.5)