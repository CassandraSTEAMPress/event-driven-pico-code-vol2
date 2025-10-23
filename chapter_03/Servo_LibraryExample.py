# servo_LibraryExample.py - SG90 servo library example
# ---------------------------------------------------------------

from time import sleep
from servo import Servo

# Create a Servo object on GPIO28
servo = Servo(pin_id=28)

# Move an SG90 Servomotor through various angles
def SG90Servo():
    
    while True: 
        # Move to 0 degrees
        servo.write(0)
        sleep(2)

        # Move to 90 degrees
        servo.write(90)
        sleep(2)

        # Move to 180 degrees
        servo.write(180)
        sleep(2)
      
if __name__ == "__main__":
    
    # Run servo
    try:
        SG90Servo()

    # Keyboard interrupt caught
    except KeyboardInterrupt:
        print("\nUser interrupted the program")

    # Unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Stop the motor
    finally:
        print("Stopping Servomotor")

        # Turn off the motor
        servo.off()
        sleep(2)

        print("\nMotor control terminated.")
