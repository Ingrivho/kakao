from Behavior import Behavior
from camera import Camera
from motor_rec import Motor_Rec
from imager2 import Imager

class driveToColor(Behavior):
    def __init__(self, sensobs, static_pri):
        super().__init__(sensobs, True, static_pri)


    def _determine_angle(self, img): # Returns an angle. negative is left, right is positive
      h = img.ymax
      half = h//2
      w = img.xmax
      img = img.crop((0,half,w,half+1)) # Img is now a one-pixel tall image, same width
      readings = []
      big_first = 0
      big_last = w-1
      big_counter = 0
      first, last, counter = 0, 0, 0

      for cur in range(w):
        rgb = img.get_pixel(cur,0)
        if rgb[0] >= 120 and rgb[1] >= 120 and rgb[2] >= 80:
          if cur - last <= 2: # If the next pixel is within 2 pixels of the last we visited
            last = cur # Flytter last frem, hvis det stemmer
            counter += 1
            if counter > big_counter: # If the current streak is bigger
               big_first = first
               big_last = last
               big_counter = counter
          else:
            first = cur
            last = cur
            counter = 0

      center = w / 2
      center_black = (big_first+big_last)//2 if big_counter >= 10 else center

      if center_black > center:
        return (round(((center_black-center)/center) * 26.75))
      else: # center_blue < center
        return (round(-((center-center_black)/center) * 26.75))


    def _update_flag(self):
      img = Imager(image=self.sensobs['camera'].get_value(), mode='RGB')
      self.angle = self._determine_angle(img)
      if abs(self.angle) > 3:
        self.active_flag = True
      else:
        self.active_flag = False


    def _sense_and_act(self):
      if self.active_flag:
        self.match_degree = 100
        direction = 'l' if self.angle > 0 else 'r'
        self.motor_recommendation.action = [direction, abs(self.angle)]
        self.motor_recommendation.description = 'Drive to color'

