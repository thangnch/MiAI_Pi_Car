import sys, tty, termios, time
import cv2
import PiCar

myCar = PiCar.PiCar()
myCar.setup()

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


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
    if char == " ":
        myCar.stop()

    # The car will drive forward when the "w" key is pressed
    if char == "w":

        myCar.drive(0)
        myCar.go_forward()

    # The car will reverse when the "s" key is pressed
    if char == "s":
        myCar.drive(0)
        myCar.go_back()

    # The "a" key will toggle the steering left
    if char == "a":
        myCar.drive(-25)

    # The "d" key will toggle the steering right
    if char == "d":
        myCar.drive(25)

    # The "x" key will break the loop and exit the program
    if char == "p":
        print("Program Ended")
        break

    char = ""
    

# Program will cease all GPIO activity before terminating
myCar.clean()
