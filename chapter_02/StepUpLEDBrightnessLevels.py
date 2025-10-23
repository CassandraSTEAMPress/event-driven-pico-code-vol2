# StepUpLEDBrightnessLevels.py - Increase the brightness of an
#   LED in noticeable steps
# ---------------------------------------------------------------

from machine import Pin, PWM
from time import sleep

# Set up PWM on Slice 7, Channel B (GPIO15), LED brightness 100%
led_brightening = PWM(Pin(15), freq=1000, duty_u16=65535)  
sleep(1)  # Delay for observing LED        

try:
    # Increase the brightness in steps
    while True:
        led_brightening.duty_u16(0)     # 0% (OFF)
        sleep(1)
        
        led_brightening.duty_u16(16384) # 25%
        sleep(1)
        
        led_brightening.duty_u16(32768) # 50%
        sleep(1)
        
        led_brightening.duty_u16(49152) # 75%
        sleep(1)
        
        led_brightening.duty_u16(65535) # 100% (ON)
        sleep(1)

# Catch keyboard interrupt         
except KeyboardInterrupt:
    print("\nProgram interrupted by user.")

# Turn off PWM         
finally:
    print("Exiting...")
    led_brightening.duty_u16(0)
    sleep(1)  # allow PWM hardware to settle
    
    led_brightening.deinit()