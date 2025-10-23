# TTMotor_ConstantSpeed.py - Rotate a TT Motor forward and
#   backward using the DRV8833
# ---------------------------------------------------------------

from machine import Pin
from time import sleep

# Specify the Pico W pins connected to the motor driver
motorA_IN1 = Pin(14, Pin.OUT)  # GPIO14
motorA_IN1.value(0)

motorA_IN2 = Pin(15, Pin.OUT)  # GPIO15
motorA_IN2.value(0)

# Stop the motor
def stop_motor():
    print("Stopping motor")
    motorA_IN1.low()
    motorA_IN2.low()
    sleep(2)  # delay after stopping

# Rotate the motor forward 
def move_forward():
    print("\nMove forward")
    motorA_IN1.high()
    motorA_IN2.low()
    print(f"motorA_IN1.high = {motorA_IN1.value()}")
    print(f"motorA_IN2.low  = {motorA_IN2.value()}")
  
# Rotate the motor backward
def move_backward():
    print("\nMove backward")
    motorA_IN1.low()
    motorA_IN2.high()
    print(f"motorA_IN1.low  = {motorA_IN1.value()}")
    print(f"motorA_IN2.high = {motorA_IN2.value()}")

# Rotate the motor the motor forward and backward at constant
#   speed
def TTMotor_constant_speed():
    move_forward()
    sleep(2)
    
    move_backward()
    sleep(2)

if __name__ == "__main__":
    
    # Run motor test
    try:
        for i in range(5):
            print(f"\nTest: {i+1}")
            print(f"=======")
            TTMotor_constant_speed()

        print("\n\n>>> End of Tests <<<")

    # Keyboard interrupt caught        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

    # Unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Stop the motor
    finally:
        # Turn off the motor
        stop_motor()
        
        print("\nMotor control terminated.")
