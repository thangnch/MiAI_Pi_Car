import RPi.GPIO as io
io.setmode(io.BCM)
import sys, tty, termios, time
import cv2
from imutils.video import VideoStream
import imutils

motor1_standard_cycle = 0
motor2_standard_cycle = 75
current_motor1_duty = 0
current_motor2_duty = 0

current_angle = 0

io.cleanup()

# Setup
motor1_in1_pin = 24
motor1_in2_pin = 23
motor1_ena_pin = 25
io.setup(motor1_in1_pin, io.OUT)
io.setup(motor1_in2_pin, io.OUT)
io.setup(motor1_ena_pin, io.OUT)

current_motor1_duty = motor1_standard_cycle
motor1 = io.PWM(motor1_ena_pin,1000)
motor1.start(current_motor1_duty)

motor2_in1_pin = 5
motor2_in2_pin = 6
motor2_ena_pin = 19
io.setup(motor2_in1_pin, io.OUT)
io.setup(motor2_in2_pin, io.OUT)
io.setup(motor2_ena_pin, io.OUT)

current_motor2_duty = motor2_standard_cycle
motor2 = io.PWM(motor2_ena_pin,1000)
motor2.start(current_motor2_duty)

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def motor1_forward():

    io.output(motor1_in1_pin, False)
    io.output(motor1_in2_pin, True)

def motor1_reverse():
    io.output(motor1_in1_pin, True)
    io.output(motor1_in2_pin, False)

def motor2_forward():
    io.output(motor2_in1_pin, False)
    io.output(motor2_in2_pin, True)

def motor2_reverse():

    io.output(motor2_in1_pin, True)
    io.output(motor2_in2_pin, False)


def motor1_stop():
    io.output(motor1_in1_pin, False)
    io.output(motor1_in2_pin, False)

def motor2_stop():
    io.output(motor2_in1_pin, False)
    io.output(motor2_in2_pin, False)

def go_forward():
    global current_motor1_duty, current_motor2_duty, current_angle
    current_angle = 0
    motor1_forward()
    motor2_forward()

def go_back():
    global current_motor1_duty, current_motor2_duty, current_angle
    motor1_reverse()
    motor2_reverse()

def stop():
    global current_motor1_duty, current_motor2_duty, current_angle
    motor1_stop()
    motor2_stop()

def drive(angle):
    global current_motor1_duty, current_motor2_duty, current_angle
    current_motor1_duty = motor1_standard_cycle
    current_motor2_duty = motor2_standard_cycle
    # angle from -5 to 5
    # turn left
    if angle<0:
        # Down the speed of motor 1
        current_motor1_duty += angle
    elif angle > 0:
        current_motor1_duty += angle

    motor2.ChangeDutyCycle(current_motor2_duty)
    motor1.ChangeDutyCycle(current_motor1_duty)

    current_angle = angle

io.output(motor1_in1_pin, False)
io.output(motor1_in2_pin, False)
io.output(motor2_in1_pin, False)
io.output(motor2_in2_pin, False)

# Instructions for when the user has an interface
print("w/s: acceleration")
print("a/d: steering")
print("space: stop")
print("c: capture photo")
print("p: exit")


while True:
    
    # Keyboard character retrieval method is called and saved
    # into variable
    char = getch()

     # The car will drive forward when the "w" key is pressed
    if(char == " "):
        stop()

    # The car will drive forward when the "w" key is pressed
    if(char == "w"):

        drive(0)
        go_forward()

    # The car will reverse when the "s" key is pressed
    if(char == "s"):
        drive(0)
        go_back()

    # The "a" key will toggle the steering left
    if(char == "a"):
        drive(-15)

    # The "d" key will toggle the steering right
    if(char == "d"):
        drive(15)

    # The "x" key will break the loop and exit the program
    if(char == "p"):
        print("Program Ended")
        break

    char = ""
    

# Program will cease all GPIO activity before terminating
io.cleanup()
