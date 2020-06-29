import RPi.GPIO as io
io.setmode(io.BCM)
import sys, tty, termios, time
import cv2
from imutils.video import VideoStream
import imutils

motor1_standard_cycle = 50
motor2_standard_cycle = 95

io.cleanup()
# These two blocks of code configure the PWM settings for
# the two DC motors on the RC car. It defines the two GPIO
# pins used for the input, starts the PWM and sets the
# motors' speed to 0
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

# The getch method can determine which key has been pressed
# by the user on the keyboard by accessing the system files
# It will then return the pressed key as a variable
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# This section of code defines the methods used to determine
# whether a motor needs to spin forward or backwards. The
# different directions are acheived by setting one of the
# GPIO pins to true and the other to false. If the status of
# both pins match, the motor will not turn.
def motor1_forward():
    io.output(motor1_in1_pin, True)
    io.output(motor1_in2_pin, False)

def motor1_reverse():
    io.output(motor1_in1_pin, False)
    io.output(motor1_in2_pin, True)

def motor2_forward():
    io.output(motor2_in1_pin, True)
    io.output(motor2_in2_pin, False)

def motor2_reverse():
    io.output(motor2_in1_pin, False)
    io.output(motor2_in2_pin, True)



# This method will toggle the direction of the steering
# motor. The method will determine whether the user wants
# to turn left or right depending on the key they press and
# then make the appropriate adjustment. It works as a toggle
# because the program cannot read multiple pressed keys at
# the same time. The possible positions of the wheels are
# "right", "centre" and "left". It will then update the
# status of the wheel to access next time it is called.
def toggleSteering(direction):

    global wheelStatus, current_motor2_duty, current_motor1_duty

    if(direction == "right"):
        if(wheelStatus == "centre"):
            motor1_forward()
            motor2_forward()
            current_motor2_duty = 0
            motor2.ChangeDutyCycle(current_motor2_duty)
            current_motor1_duty = motor1_standard_cycle
            motor1.ChangeDutyCycle(current_motor1_duty)
            wheelStatus = "right"
        elif(wheelStatus == "left"):
            current_motor2_duty = motor2_standard_cycle
            motor2.ChangeDutyCycle(current_motor2_duty)
            current_motor1_duty = motor1_standard_cycle
            motor1.ChangeDutyCycle(current_motor1_duty)
            wheelStatus = "centre"

    if(direction == "left"):
        if(wheelStatus == "centre"):
            motor1_forward()
            motor2_forward()
            current_motor1_duty = 0
            motor1.ChangeDutyCycle(current_motor1_duty)
            current_motor2_duty = motor2_standard_cycle
            motor2.ChangeDutyCycle(current_motor2_duty)
            wheelStatus = "left"
        elif(wheelStatus == "right"):
            current_motor1_duty = motor1_standard_cycle
            motor1.ChangeDutyCycle(current_motor1_duty)
            current_motor2_duty = motor2_standard_cycle
            motor2.ChangeDutyCycle(current_motor2_duty)
            wheelStatus = "centre"

# Setting the PWM pins to false so the motors will not move
# until the user presses the first key
io.output(motor1_in1_pin, False)
io.output(motor1_in2_pin, False)
io.output(motor2_in1_pin, False)
io.output(motor2_in2_pin, False)

# Global variables for the status of the lights and steering
lightStatus = False
wheelStatus = "centre"

# Instructions for when the user has an interface
print("w/s: acceleration")
print("a/d: steering")
print("space: stop")
print("c: capture photo")
print("p: exit")


vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(1.0)

while True:
    
    # Keyboard character retrieval method is called and saved
    # into variable
    char = getch()

     # The car will drive forward when the "w" key is pressed
    if(char == " "):
        io.output(motor1_in1_pin, False)
        io.output(motor1_in2_pin, False)
        io.output(motor2_in1_pin, False)
        io.output(motor2_in2_pin, False)
        wheelStatus = "centre"

    # The car will drive forward when the "w" key is pressed
    if(char == "w"):
        motor2_forward()
        motor1_forward()
        motor1.ChangeDutyCycle(motor1_standard_cycle)
        motor2.ChangeDutyCycle(motor2_standard_cycle)
        wheelStatus = "centre"
        #motor2.ChangeDutyCycle(99)

    # The car will reverse when the "s" key is pressed
    if(char == "s"):
        motor2_reverse()
        motor1_reverse()
        motor2.ChangeDutyCycle(motor2_standard_cycle-5)
        motor1.ChangeDutyCycle(motor1_standard_cycle)
        wheelStatus  ="centre"
        #motor2.ChangeDutyCycle(99)

    # The "a" key will toggle the steering left
    if(char == "a"):
        toggleSteering("left")

    # The "d" key will toggle the steering right
    if(char == "d"):
        toggleSteering("right")
    if(char == "c"):
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        cv2.imshow("Frame", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



    # The "x" key will break the loop and exit the program
    if(char == "p"):
        print("Program Ended")
        break

    # At the end of each loop the acceleration motor will stop
    # and wait for its next command
    #motor2.ChangeDutyCycle(0)
    #motor1.ChangeDutyCycle(0)

    # The keyboard character variable will be set to blank, ready
    # to save the next key that is pressed
    char = ""
    

# Program will cease all GPIO activity before terminating
io.cleanup()
cv2.destroyAllWindows()
vs.stop()