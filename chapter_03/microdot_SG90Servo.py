"""
microdot_SG90Servo.py
--------
Rotate a servo through various angles

Use a Microdot webserver to provide data consumers with
  event details
"""
# ---------------------------------------------------------------

from time import sleep
from servo import Servo
import asyncio, webserver_Servo, config_servo

# Create a Servo object on GPIO28
servo = Servo(pin_id=config_servo.pin_id)

"""Move an SG90 Servomotor through various angles"""
async def SG90Servo():
    
    while True:
        
        # Move to 0 degrees
        config_servo.servo_angle = 0
        servo.write(config_servo.servo_angle)
        await asyncio.sleep(2)  # yield control to the event loop

        # Move to 90 degrees
        config_servo.servo_angle = 90
        servo.write(config_servo.servo_angle)
        await asyncio.sleep(2)

        # Move to 180 degrees
        config_servo.servo_angle = 180
        servo.write(config_servo.servo_angle)
        await asyncio.sleep(2)  

# Main entry point for the event loop
async def main():
    print("Starting async tasks ...")

    web_server = asyncio.create_task( \
        webserver_Servo.start_server())
    SG90_task = asyncio.create_task(SG90Servo())                                 
    await asyncio.gather(SG90_task, web_server)

if __name__ == "__main__":
    
    # Start event loop
    try:
        main_task=asyncio.run(main())

    # Keyboard interrupt caught
    except KeyboardInterrupt:
        print("\nUser interrupted the program")

    # Unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Stop the motor
    finally:
        print("Stopping motor")

        # Turn off the motor
        servo.off()
        sleep(2)

        print("\nMotor control terminated.")