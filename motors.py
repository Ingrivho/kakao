#!/usr/bin/env python
from time import sleep
import RPi.GPIO as GPIO
import wiringpi2 as wp
from random import randint


class Motors():
  def __init__(self):
    self.setup()

  def setup(self):
    self.max = 1024
    self.high = 500
    self.normal = 300
    self.low = 100
    self.turnRate = 600;
    self.turnDur = 12;
    self.lastTurn = "r"

    wp.wiringPiSetupGpio()

    wp.pinMode(18, 2)
    wp.pinMode(19, 2)
    wp.pinMode(23, 1)
    wp.pinMode(24, 1)

    self.set_left_dir(0)  # Set rotation direction to forward for both wheels
    self.set_right_dir(0)

    self.freq = 400  # PWM frequency
    self.dc = 0  # Duty cycle
    print("Completed setting up motors!")

    # For the following motion commands, the speed is in the range [-1, 1], indicating the fraction of the maximum
    # speed, with negative values indicating that the wheel will spin in reverse. The argument "dur" (duration)
    # is the time (in seconds) that the action will persist.

  def forward(self, speed=0.25, dur=None):
    self.dc = int(self.max * speed)
    self.set_left_dir(0)
    self.set_right_dir(0)
    self.set_left_speed(self.dc)
    self.set_right_speed(self.dc)
    self.persist(dur)

  def backward(self, speed=0.25, dur=None):
    self.set_left_dir(1)
    self.set_right_dir(1)
    self.dc = int(self.max * speed)
    self.set_left_speed(self.dc)
    self.set_right_speed(self.dc)
    self.dc = int(self.max * speed)

    self.persist(dur)

  def left(self, speed=0.25, dur=None):
    s = int(self.max * speed)
    if self.dc == 0:
      self.set_left_dir(1)
      self.set_left_speed(s)
      self.set_right_dir(0)
      self.set_right_speed(s)
    else:
      self.set_left_speed(150)
      self.set_right_speed(450)
    self.persist(dur)

  def right(self, speed=0.25, dur=None):
    s = int(self.max * speed)
    if self.dc == 0:
      self.set_left_dir(0)
      self.set_left_speed(s)
      self.set_right_dir(1)
      self.set_right_speed(s)
    else:
      self.set_left_speed(450)
      self.set_right_speed(150)
      self.persist(dur)


  def stop(self):
    self.dc = 0
    self.set_left_speed(self.dc)
    self.set_right_speed(self.dc)

    # Val should be a 2-element vector with values for the left and right motor speeds, both in the range [-1, 1].
  def set_value(self, val,dur=None):
    left_val = int(self.max * val[0])
    right_val = int(self.max * val[1])

        # If we pass negative values to the motors, we need to reverse the direction of the motor
    self.set_left_dir(1) if (left_val < 0) else self.set_left_dir(0)
    self.set_right_dir(1) if (right_val < 0) else self.set_right_dir(0)

        # Set speed to the absolute value of the passed values
    self.set_left_speed(abs(left_val))
    self.set_right_speed(abs(right_val))
    self.persist(dur)

    # These are lower-level routines that translate speeds and directions into write commands to the motor output pins.

  def set_left_speed(self, dc):
    wp.pwmWrite(18, dc)

  def set_right_speed(self, dc):
    wp.pwmWrite(19, dc)

  def set_left_dir(self, is_forward):
    wp.digitalWrite(23, is_forward)  # 0 is forward so if they pass 1 we 'not' it

  def set_right_dir(self, is_forward):
    wp.digitalWrite(24, is_forward)  # 0 is forward so if they pass 1 we 'not' it


  def persist(self, duration):
    if duration:
      sleep(duration)
      self.stop()

  def setMax(self,max):
    self.max = max;

  def do(self, action):
    if type(action) == int:
      if action> 0:
        self.forward(action)
      else:
        s = action * -1
        self.backward(action)

    elif (type(action) == list):
      dir = action[0];
      if(dir == "r" or dir == "l"):
        self.turnAround(dir,action[1]);
    elif (type(action) == str):
      if(action =="b"):
        self.backAndTurn();


  def turnAround(self,dir,degrees):
    if(dir=="r"):
      self.set_left_dir(1)
      self.set_left_speed(self.turnRate)
      self.set_right_dir(0)
      self.set_right_speed(self.turnRate)
    elif(dir=="l"):
      self.set_left_dir(0)
      self.set_left_speed(self.turnRate)
      self.set_right_dir(1)
      self.set_right_speed(self.turnRate)
    self.persist(degrees*self.turnDur/self.turnRate); #her må vi nok tweeke slik at det passer antall grader. Persist gjør at den utfører handlingen i gitt tid.			

  def backAndTurn(self):
    self.stop();
    self.backward(1,1);
    dir = self.getRandomDir()
    degrees = randint(90,270)
    self.turnAround(dir,degrees);
    
  
  def getRandomDir(self):
    if randint(0,1) == 1:
      return "l"
    return "r"
    
   
  def setTurnSpeed(self,turnRate):
    self.turnRate = turnRate;
    
  def setTurnDur(self,turnDur):
    self.turnDur = turnDur;
