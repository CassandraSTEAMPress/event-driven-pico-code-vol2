"""
microdot_TTMotor.py
--------
Rotate a TT Motor forward at different speeds in FAST decay mode:
  IN1=PWM, IN2=0

Use a Microdot webserver to provide data consumers with event
  details
"""
# ---------------------------------------------------------------

from machine import Pin, PWM
from time import sleep
import asyncio, webserver_TTMotor, config_ttmotor

# Specify the Pico W pins connected to the motor driver
motorA_IN1 = Pin(config_ttmotor.motorA_IN1, Pin.OUT)  # GPIO14
motorA_IN1.value(0)

motorA_IN2 = Pin(config_ttmotor.motorA_IN2, Pin.OUT)  # GPIO15
motorA_IN2.value(0)

# Create a PWM instance for controlling the motor's speed
motorA_IN1_PWM = PWM(motorA_IN1, freq=config_ttmotor.motorA_freq)
motorA_IN1_PWM.duty_u16(0)

# Direction (informational)
motorA_direction = config_ttmotor.motorA_direction
motorA_decay_mode = config_ttmotor.motorA_decay_mode

# Stop the motor
def stop_motor():
    print("Stopping motor")
    motorA_IN1.value(0)  
    motorA_IN2.value(0)  
    motorA_IN1_PWM.duty_u16(0)
    sleep(1)  # allow PWM hardware time to settle

    # Turn off PWM
    motorA_IN1_PWM.deinit()
    
"""Rotate the motor at different speeds"""
async def TTMotor():

    while True:
        # 40% Speed: 26214/65535
        speed_u16=26214  
        motorA_IN1_PWM.duty_u16(speed_u16)
        config_ttmotor.motorA_speed = \
                                    f"{speed_u16/65535*100:.2f}%"
        print(f"Motor speed: {config_ttmotor.motorA_speed}")
        await asyncio.sleep(2)  # yield control to the event loop
        
        # 60% Speed: 39321/65535
        speed_u16=39321
        motorA_IN1_PWM.duty_u16(speed_u16)
        config_ttmotor.motorA_speed = \
                                    f"{speed_u16/65535*100:.2f}%"
        print(f"Motor speed: {config_ttmotor.motorA_speed}")
        await asyncio.sleep(2)  # yield control to the event loop
        
        # 80% Speed: 52428/65535
        speed_u16=52428
        motorA_IN1_PWM.duty_u16(speed_u16)
        config_ttmotor.motorA_speed = \
                                    f"{speed_u16/65535*100:.2f}%"
        print(f"Motor speed: {config_ttmotor.motorA_speed}")
        await asyncio.sleep(2)  # yield control to the event loop
        
        # 100% Speed: 65535/65535
        speed_u16=65535
        motorA_IN1_PWM.duty_u16(speed_u16)
        config_ttmotor.motorA_speed = \
                                    f"{speed_u16/65535*100:.2f}%"
        print(f"Motor speed: {config_ttmotor.motorA_speed}")
        await asyncio.sleep(2)  # yield control to the event loop

# Main entry point for the event loop      
async def main():
    print("Starting async tasks ...")

    web_server = asyncio.create_task( \
        webserver_TTMotor.start_server())
    TTMotor_task = asyncio.create_task(TTMotor())
                                        
    await asyncio.gather(TTMotor_task, web_server)

if __name__ == "__main__":
    
    # Start event loop
    try:
        main_task=asyncio.run(main())

    # Keyboard interrupt caught
    except KeyboardInterrupt:
        print("TTMotor test interrupted by user.")

    # Unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    # Stop the motor
    finally:
        # Turn off the motor
        stop_motor()

        print("\nMotor control terminated.")