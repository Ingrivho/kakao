from sensors import *
from sensobs import *
from behaviors import *
from arbitrator import Arbitrator
from motob import Motob
from BBCON import Bbcon


def main():

    ultrasonic_sensor = Ultrasonic()
    camera_sensor = Camera()
    reflectance_sensor = ReflectanceSensors()
    print('Made sensors')

    ultrasonic_sensob = Sensob(ultrasonic_sensor)
    camera_sensob = CameraSensob(camera_sensor)
    reflectance_sensob = ReflectanceSensob(reflectance_sensor)
    sensobs = [ultrasonic_sensob, camera_sensob, reflectance_sensob]
    print('Made sensobs')

    ultrasonic_behavior = SonicBehavior(ultrasonic_sensob)
    camera_behavior = CameraBehavior(camera_sensob, 1.0)
    reflectance_behavior = ReflectanceSensorsBehavior(reflectance_sensob)
    behaviors = [ultrasonic_behavior, camera_behavior, reflectance_behavior]
    print('Made behaviors')

    arbitrator = Arbitrator()
    print('Made arbitrator')

    motob = Motob()
    print('Made motob')

    bbcon = Bbcon(behaviors, sensobs, motob, arbitrator)
    print('Made BBCON')

    print('Running...')
    try:
        while True:
            bbcon.run_one_timestep()
    except:
        bbcon.motob.m.stop()
        print('Exited')


if __name__ == '__main__':
    main()
