# PWMExample_FadingLED.py - Fade an LED using
#   PWM Slice 7 Channel B 
# ---------------------------------------------------------------

from machine import Pin, PWM
from time import sleep

# Set up PWM on Slice 7, Channel B (GPIO15), LED brightness 100%
led_fading = PWM(Pin(15), freq=1000, duty_u16=65535)
sleep(1)   # Delay for observing LED

try:
    # Fade the LED gradually
    fade_step = 255  # 0.39% (=255/65535)
    while True:        
        for duty_cycle in range(65535, -1, -fade_step):
            led_fading.duty_u16(duty_cycle)
            sleep(0.01)

# Catch keyboard interrupt         
except KeyboardInterrupt:
    print("\nProgram interrupted by user.")

# Turn off PWM 
finally:
    print("Exiting...")
    led_fading.duty_u16(0)
    sleep(1)  # allow PWM hardware to settle
    
    led_fading.deinit()