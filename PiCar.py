import RPi.GPIO as io
#import time
io.setmode(io.BCM)
#50-95

class PiCar(object):
    def __init__(self, motor1_standard_cycle=25, motor2_standard_cycle=45):
        self.max_turn_angle = 4
        self.motor1_standard_cycle = motor1_standard_cycle
        self.motor2_standard_cycle = motor2_standard_cycle
        self.current_motor1_duty = 0
        self.current_motor2_duty = 0
        self.current_angle = 0

        self.motor1_in1_pin = 24
        self.motor1_in2_pin = 23
        self.motor1_ena_pin = 25

        self.motor2_in1_pin = 5
        self.motor2_in2_pin = 6
        self.motor2_ena_pin = 19

        self.motor1 = None
        self.motor2 = None

    def setup(self):

        print("Init call")
        # Set ports for motor1

        io.setup(self.motor1_in1_pin, io.OUT)
        io.setup(self.motor1_in2_pin, io.OUT)
        io.setup(self.motor1_ena_pin, io.OUT)

        # Set power for motor1
        self.current_motor1_duty = self.motor1_standard_cycle
        self.motor1 = io.PWM(self.motor1_ena_pin, 1000)
        self.motor1.start(self.current_motor1_duty)


        # Set ports for motor2

        io.setup(self.motor2_in1_pin, io.OUT)
        io.setup(self.motor2_in2_pin, io.OUT)
        io.setup(self.motor2_ena_pin, io.OUT)

        # Set power motor2
        self.current_motor2_duty = self.motor2_standard_cycle
        self.motor2 = io.PWM(self.motor2_ena_pin, 1000)
        self.motor2.start(self.current_motor2_duty)

        #self.motor1_stop()
        #self.motor2_stop()

    def clean(self):
        self.current_motor2_duty = 0
        self.current_motor1_duty = 0
        io.cleanup()
        print("Clean")



    def go_forward(self):
        self.current_angle = 0
        self.motor1_forward()
        self.motor2_forward()

    def go_back(self):
        self.motor1_reverse()
        self.motor2_reverse()

    def stop(self):
        self.motor1_stop()
        self.motor2_stop()

    def drive(self, angle):
        self.current_motor1_duty = self.motor1_standard_cycle
        self.current_motor2_duty = self.motor2_standard_cycle
        print("Angle b:",angle)
        # angle from -25 to 25

        if angle<90:
            angle = -(angle/90)*(self.max_turn_angle/2)
        else:
            angle = ((angle-90)/90)*(self.max_turn_angle/2)
        # turn left

        print("Angle a:", angle)

        if angle<0:
            # Down the speed of motor 1
            self.current_motor1_duty += angle
        elif angle == 0:
            self.current_motor1_duty = self.motor1_standard_cycle
            self.current_motor2_duty = self.motor2_standard_cycle
        else:
            self.current_motor2_duty -= angle

        print("curr M2:", self.current_motor2_duty)
        print("curr M1:", self.current_motor1_duty)

        self.motor2.ChangeDutyCycle(self.current_motor2_duty)
        self.motor1.ChangeDutyCycle(self.current_motor1_duty)

        self.current_angle = angle

    def clear_io(self):
        io.cleanup()

    def motor1_forward(self):
        io.output(self.motor1_in1_pin, True)
        io.output(self.motor1_in2_pin, False)

    def motor1_reverse(self):
        io.output(self.motor1_in1_pin, False)
        io.output(self.motor1_in2_pin, True)

    def motor2_forward(self):
        io.output(self.motor2_in1_pin, True)
        io.output(self.motor2_in2_pin, False)

    def motor1_stop(self):
        io.output(self.motor1_in1_pin, False)
        io.output(self.motor1_in2_pin, False)

    def motor2_reverse(self):
        io.output(self.motor2_in1_pin, False)
        io.output(self.motor2_in2_pin, True)

    def motor2_stop(self):
        io.output(self.motor2_in1_pin, False)
        io.output(self.motor2_in2_pin, False)
'''
mycar = PiCar()
mycar.setup()
mycar.go_forward()
time.sleep(3.0)
mycar.stop()
mycar.clean()
print("DOne")
'''