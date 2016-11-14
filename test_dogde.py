from ultrasonic import *

class Test_dogde():
	def __init__(self):
		self.priority = 1;
		self.ultrasonic = Ultrasonic();
	
	def get_suggestion(self):
		speed_value = 100;
		turn_value = 0.0;
		score=10;
		distance = self.ultrasonic.update();
		print("distance: " + str(distance));
		
		if(distance<10 and distance>0):
			speed_value = -(5/distance);
		elif distance<15 and distance>0:
			speed_value = 0;
		elif(distance<40 and distance>0):
			speed_value =(float((distance)/30)); 
		
		return score,speed_value,turn_value;

		