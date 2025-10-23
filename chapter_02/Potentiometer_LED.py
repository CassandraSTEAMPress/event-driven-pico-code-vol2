# Potentiometer_LED.py - Use PWM to vary LED brightness with a
#   potentiometer
# ---------------------------------------------------------------

from machine import Pin, PWM, ADC
from time import sleep

# Set up PWM on Slice 7, Channel B (GPIO15), LED brightness 100%
led_fading = PWM(Pin(15), freq=1000, duty_u16=65535)

# Use GPIO28 to read analog output voltage from a potentiometer
pot = ADC(Pin(28))

# Change the LED brightness with the potentiometer 
try:
    while True:
        pot_value = pot.read_u16()       # get duty cycle
        led_fading.duty_u16(pot_value)   # set duty cycle
        print(f'duty cycle = {pot_value}: '
              f'{round((pot_value/65535)*100)}%')
        sleep(0.1)
    
except KeyboardInterrupt:
    print("\nProgram interrupted by user.")

# Turn off PWM        
finally:
    print("Exiting...")
    led_fading.duty_u16(0)
    sleep(1)  # allow PWM hardware time to settle
    
    led_fading.deinit()    