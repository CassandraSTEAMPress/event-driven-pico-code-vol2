# servo_BasicExample.py - A very basic SG90 Servo example
# ---------------------------------------------------------------

from machine import Pin, PWM
from time import sleep

# Angle range: 0 to 180 degrees
ANGLE_MIN = 0
ANGLE_MAX = 180

MIN_PULSE_US = 500   # minimum pulse duration for 0 degrees
MAX_PULSE_US = 2500  # maximum pulse duration for 180 degrees

# Set up a PWM Pin to control the servo
servo_control_pin = Pin(28, Pin.OUT)     # GPIO28
servo = PWM(servo_control_pin, freq=50)  # PWM Frequency = 50Hz

# Convert angle (0-180 degrees) to a pulse duration.
def angle_to_pulse_width(angle):
    if (angle < ANGLE_MIN) or (angle > ANGLE_MAX):
        raise ValueError("Angle out of range")

    # Compute pulse duration in us
    pulse_duration_us = MIN_PULSE_US + (angle * \
                        (MAX_PULSE_US - MIN_PULSE_US) / 180.0)

    # Convert microseconds to a duty cycle value
    #   (0-65535 for 16-bit PWM), Pulse period = 20 ms
    return int(pulse_duration_us * 65535 / 20000)

# Stop the motor
def stop_motor():
    print("Stopping motor")

    servo_control_pin.value(0)
    servo.duty_u16(0)
    sleep(1)  # allow PWM hardware time to settle

    # Turn off PWM
    servo.deinit()

# Move an SG90 Servomotor through various angles
def SG90Servo():

    while True:
        # Move to 0 degrees
        servo.duty_u16(angle_to_pulse_width(0))
        sleep(2)

        # Move to 90 degrees
        servo.duty_u16(angle_to_pulse_width(90))
        sleep(2)

        # Move to 180 degrees
        servo.duty_u16(angle_to_pulse_width(180))
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

    # Stop motor control
    finally:
        # Turn off the motor
        stop_motor()

        print("\nMotor control terminated.")
