#!/usr/bin/env python
import datetime
import os
from PIL import Image
from abc import abstractmethod
import RPi.GPIO as GPIO
import time
import wiringpi as wp


class Sensor:
    @abstractmethod
    def update(self):
        pass


class Ultrasonic(Sensor):
    def __init__(self):

        self.value = None

        # These should correspond to the GPIO pins connected to trig and echo on the sensor.

        self.trig_pin = 26
        self.echo_pin = 11
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_value(self):

        return self.value

    def update(self):

        self.value = self.sensor_get_value()

        return self.value

    def reset(self):

        self.value = None

    def sensor_get_value(self):

        self.send_activation_pulse()

        # Sensoren starter saa programmet sitt.
        # Det den gjor er aa sende ut 8 sykler av et ultrasonisk signal paa 40kHz.
        # Den venter saa paa at signalet skal bli reflektert tilbake til leseren.

        # Vi leser signalet den mottar paa echo_pin
        read_val = GPIO.input(self.echo_pin)

        # Det som er interessent her er hvor lang tid det tar fra signalet er sendt ut, til noe er returnert
        # Naar sensoren mottar et reflektert signal vil echo pinnen settes hoy like lang tid som
        # signalet brukte fra det ble sendt ut til det ble returnert

        # Vi finner tiden paa siste gang echo signalet er lavt
        signaloff_start = time.time()

        signaloff = signaloff_start

        # signalet timer ut dersom det tar mer en 0.5 s, da annsees det som tapt og vi prover igjen
        while read_val == 0 and signaloff - signaloff_start < 0.5:
            read_val = GPIO.input(self.echo_pin)
            signaloff = time.time()

        signalon = signaloff

        # Finner saa den tiden det siste signalet kommer inn paa echo_pin
        while read_val == 1:
            read_val = GPIO.input(self.echo_pin)
            signalon = time.time() # Kan flytte denne ut av loopen dersom det skaper delay og unoyaktighet

        # Den kalkulerte avstanden
        distance = self.compute_distance(signalon, signaloff)

        # Returnerer distanset til objektet forran sensoren i cm
        return distance

    def send_activation_pulse(self):
        GPIO.output(self.trig_pin, GPIO.LOW)
        # Sensoren kan krasje dersom man ikke har et delay her. Dersom den fortsatt krasjer, prov aa oke delayet
        time.sleep(0.3)

        # Ultralyd-sensoren starter naar den mottar en puls, med lengde 10uS paa trig pinnen.
        # Vi gjor dette ved aa sette trig_pin hoy, venter i 10uS og setter den lav igjen.
        GPIO.output(self.trig_pin, True)

        # 0.00001 seconds = 10 micro seconds
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

    def compute_distance(self, signalon, signaloff):
        #print('on: ',signalon, ' off: ',signaloff)

        # Tiden det tok fra signalet ble sendt til det ble returnert
        timepassed = signalon - signaloff

        # Vi vet at signalet gaar med lydens hastighet som er ca 344 m/s
        # Avstanden til objektet forran sensoren kan vi da finne med formelen: strekning = hastighet * tid
        distance = 344 * timepassed * 100

        # Dette er tur retur distansen. For aa faa distansen en vei deler vi bare paa 2
        distance /= 2
        return distance


class ZumoButton():
    def __init__(self):
        wp.wiringPiSetupGpio()
        wp.pinMode(22, 0)
        wp.pullUpDnControl(22, 2)

    def wait_for_press(self):
        read_val = wp.digitalRead(22)
        while read_val:
            read_val = wp.digitalRead(22)
        print("Button pressed!!")


class ReflectanceSensors():
    # The constructor allows students to decide if they want to auto_calibrate
    # the robot, or if they want to hard code the min and max readings of the
    # reflectance sensors
    def __init__(self, auto_calibrate=False, min_reading=100, max_reading=1000):
        self.setup()
        if (auto_calibrate):
            # Calibration loop should last ~5 seconds
            # Calibrates all sensors
            for i in range(5):
                self.calibrate()
                time.sleep(1)
        else:
            for i in range(len(self.max_val)):
                self.max_val[i] = max_reading
                self.min_val[i] = min_reading

        print("Calibration results")
        print(self.max_val)
        print(self.min_val)

    def setup(self):
        # Initialize class variables
        self.max_val = [-1, -1, -1, -1, -1, -1]
        self.min_val = [-1, -1, -1, -1, -1, -1]
        self.start_time = -1
        # Initialize value array to all negative values, which should never appear
        # as an actual result
        self.value = [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0]
        # A dictionary mapping each channel to the index it's value is located in
        # the value array
        self.sensor_indices = {29: 5, 36: 4, 37: 3, 31: 2, 32: 1, 33: 0}
        self.updated = False
        # For GPIO.BOARD
        self.sensor_inputs = [33, 32, 31, 37, 36, 29]  # Sensors from left to right

        # Set the mode to GPIO.BOARD
        GPIO.setmode(GPIO.BOARD)

    def calibrate(self):
        print("calibrating...")
        self.recharge_capacitors()

        # GPIO.setup(sensor_inputs, GPIO.IN)
        for pin in self.sensor_inputs:
            time = self.get_sensor_reading(pin)

            # Get the index from the map
            index = self.sensor_indices[pin]

            # This is the first iteration
            if (self.max_val[index] == -1):
                self.max_val[index] = time.microseconds
                self.min_val[index] = time.microseconds
            else:
                # Store the min and max values seen during calibration
                if (time.microseconds > self.max_val[index]):
                    self.max_val[index] = time.microseconds
                elif (time.microseconds < self.min_val[index]):
                    self.min_val[index] = time.microseconds

            # Print the calculated time in microseconds
            print("Pin: " + str(pin))
            print(time.microseconds)

    def get_sensor_reading(self, pin):
        GPIO.setup(pin, GPIO.IN)
        # Measure the time
        start_time = datetime.datetime.now()

        while GPIO.input(pin):
            pass

        # Measure time again
        end_time = datetime.datetime.now()
        # Calculate the time passed
        time = end_time - start_time
        return time

    def recharge_capacitors(self):
        # Make all sensors an output, and set all to HIGH
        GPIO.setup(self.sensor_inputs, GPIO.OUT)
        GPIO.output(self.sensor_inputs, True)
        # Wait 5 milliseconds to ensure that the capacitor is fully charged
        time.sleep(0.005)

    def reset(self):
        self.updated = False
        self.value = [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0]

    # Function should return a list of 6 reals between 0 and 1.0 indicating
    # the amount of reflectance picked up by each one.  A high reflectance (near 1) indicates a LIGHT surface, while
    # a value near 0 indicates a DARK surface.

    def get_value(self):
        return self.value

    def update(self):
        self.compute_value()
        return self.value

    def compute_value(self):
        self.recharge_capacitors()
        for pin in self.sensor_inputs:
            time = self.get_sensor_reading(pin)

            index = self.sensor_indices[pin]
            self.value[index] = 1 - self.normalize(index, time.microseconds)

    # Uses the calibrated min and maxs for each sensor to return a normalized
    # value for the @param sensor_time for the given @param index
    def normalize(self, index, sensor_time):
        normalized_value = float(sensor_time) / (self.max_val[index] - self.min_val[index])
        if (normalized_value > 1.0):
            return 1.0
        elif (normalized_value < 0.0):
            return 0.0
        return normalized_value


class Camera:
    def __init__(self, img_width=128, img_height=96, img_rot=0):
        self.value = None
        self.img_width = img_width
        self.img_height = img_height
        self.img_rot = img_rot

    def get_value(self):
        return self.value

    def update(self):
        self.sensor_get_value()
        return self.value

    def reset(self):
        self.value = None

    def sensor_get_value(self):
        # This is a OS call that takes a image and makes it accessible to PIL operations in the same directory
        os.system('raspistill -t 1 -o image.png -w "' + str(self.img_width) + '" -h "' + str(self.img_height) + '" -rot "' + str(self.img_rot) + '"')
        # Open the image just taken by raspicam
        # Stores the RGB array in the value field
        self.value = Image.open('image.png').convert('RGB')

# Just testing the camera in python
# os.system('raspistill -t 1 -o image.png -w "' + str(200) + '" -h "' + str(200) + '" -rot "' + str(0) + '"')
