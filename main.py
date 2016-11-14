from motors import Motors
from zumo_button import ZumoButton
from time import sleep
from test_dogde import Test_dogde
form time import sleep

def Start():
	ZumoButton().wait_for_press();
	sleep(3);
	m = Motors();
	m.setMax(250);
	d = Test_dogde();
	while(not ZumoButton().button_pressed()):
		score,speed_value,turn_value = d.get_suggestion();
		
		print("forward" + str(speed_value));
		if speed_value<0:
			print("RYGG!!");
			m.backward(-1*speed_value);
		else:
			m.right(0.4,1);
		print("turn");
		sleep(1);
		

Start();