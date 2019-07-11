import Adafruit_CharLCD as LCD
import geocoder
import pyowm
import time
import logging
from threading import Thread, Timer, Condition, Lock

class weatherDisplay(Thread):
    def __init__(self, apiKey, poolRate=10, dispPins=None, autoStart=True):
        self.runThread = True
        self.displayLocation = ""
        self.displayString = ""
        self.apiKey = apiKey
        self.poolRate = poolRate
        self.runFlag = autoStart
        # Assign pins if empty
        if dispPins == None:
            dispPins = { "rs": 22, "en": 17, "d7": 18, "d6": 23, "d5": 24, "d4": 25 }
        
        self._initDisplay(dispPins)
        Thread.__init__(self)
        self.sleep_lock = Lock()
        self.sleep_cond = Condition(self.sleep_lock)
        self.start()
        self.logger = logging.getLogger("iwWeather")
        self.logger.info("Weather thread started!")
     
    def run(self):
        self._fetchWeather()
        iteration = 0
        try:
            while self.runThread:
                if not self.runFlag:
                    self.sleep_lock.acquire()
                    self.sleep_cond.wait()
                # Weather scrolling text algorithm below
                if len(self.displayString) < 16:
                    weatherString = self.displayString
                else:
                    dispRange = iteration%len(self.displayString)
                    if dispRange + 15 < len(self.displayString):
                        weatherString = self.displayString[dispRange:dispRange+16]
                    else:
                        divisionPoint = 16 - (len(self.displayString) - dispRange)
                        weatherString = self.displayString[dispRange:len(self.displayString)] + " " + self.displayString[0:divisionPoint-1]
                self._drawScreen(self.displayLocation, weatherString)
                iteration+=1
                time.sleep(1)
        finally:
            # Clean up procedure
            self.disp.clear()
            self.logger.info("Thread killed running release!")
            self.sleep_lock.release()

    def stopWatch(self):
        self.timer.cancel()
        self.runFlag = False

    def startWatch(self):
        self.runFlag = True
        self._fetchWeather()
        if not self.sleep_lock.locked():
            self.sleep_lock.acquire()
        self.sleep_cond.notify()
        self.sleep_lock.release()
        self.logger.info("Restarted the thread!")

    def stopThread(self):
        self.logger.info("Stopping and killing the thread!")
        if not self.sleep_lock.locked():
            self.sleep_lock.acquire()
        self.runFlag = True
        self.runThread = False
        self.timer.cancel()
        # restart running in case the thread was sleeping in wait condition
        self.sleep_cond.notify()

    def _initDisplay(self, dispPins):
        self.disp = LCD.Adafruit_CharLCD(dispPins['rs'], dispPins['en'], dispPins['d4'], dispPins['d5'], dispPins['d6'], dispPins['d7'], 16, 2)

    def _fetchWeather(self):
        geo = geocoder.ip('me')
        currentCoordinates = geo.latlng

        owm = pyowm.OWM(self.apiKey)  # You MUST provide a valid API key
        observation = owm.weather_at_coords(currentCoordinates[0], currentCoordinates[1])
        weather = observation.get_weather()

        self.displayLocation = geo.city+','+geo.country
        self.displayString = 'Temperature: '+str(weather.get_temperature('celsius')['temp'])+\
            ' Pressure: '+str(weather.get_pressure()['press'])

        # Recursion starts here
        self.timer = Timer(self.poolRate, self._fetchWeather)
        self.timer.start()

    def _drawScreen(self, upperString, lowerString):
        self.disp.clear()
        self.disp.message(upperString)
        self.disp.set_cursor(0, 1)
        self.disp.message(lowerString)