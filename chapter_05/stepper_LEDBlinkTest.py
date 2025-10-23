# stepper_LEDBlinkTest.py - Check Pico connection to    
#   the ULN2003 Motor Board by blinking the LEDs
# ---------------------------------------------------------------

from machine import Pin
from time import sleep

# Define GPIO pins connected to the input pins (IN1-IN4) of the
#   ULN2003 Motor Driver
IN1 = Pin(21, Pin.OUT)  # GPIO21
IN2 = Pin(20, Pin.OUT)
IN3 = Pin(19, Pin.OUT)
IN4 = Pin(18, Pin.OUT)
MOTOR_CHANNELS = [IN1, IN2, IN3, IN4]

# Turn off all the motor channels
def stop_motor_channels():
    for input_pin in MOTOR_CHANNELS:
        input_pin.value(0)  # turn off motor channel LED
        
# Blink Motor Board LEDs in sequence
def blink_motor_channels():
    while True:
        for input_pin in MOTOR_CHANNELS:
            input_pin.value(1)
            sleep(0.25)
            input_pin.value(0)
            sleep(0.25)

if __name__ == "__main__":
    # Pico onboard LED
    pico_led = Pin("LED", Pin.OUT)

    # Turn on Pico onboard LED
    pico_led.on()
    
    try:
        # Blink motor channel LEDs in sequence
        blink_motor_channels()
            
    # Keyboard interrupt caught
    except KeyboardInterrupt:
        print("\nUser interrupted the program")
        
    # Unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Stop the motor gracefully
    finally:
        print("Turning off motor channel LEDs")

        # Turn off the motor channels
        stop_motor_channels()

        print("\nMotor control terminated.")

    # Turn off Pico onboard LED
    pico_led.off()
