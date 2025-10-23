# BreathingLED.py - Vary the brightness levels of two LEDs in the
#   same PWM slice but change the brightness of one of the LEDs
#   with a potentiometer
# ---------------------------------------------------------------

from machine import Pin, PWM, ADC
from time import sleep

# Set up PWM on Slice 7 (GPIO14 and GPIO15, LED brightness at
#   half max (duty cycle = 50%) for both
led_fading = PWM(Pin(14), freq=1000, duty_u16=32768)
led_pot = PWM(Pin(15), freq=1000, duty_u16=32768)
sleep(3)             

# Vary the brightness level of the first LED but change 
#   the brightness of the second LED with the potentiometer
try:
    pot = ADC(Pin(28))  # potentiometer
    fade_step = 255     
    while True:
        # Breathe in: Increase the duty cycle of the first LED
        #   to 100%
        for duty_cycle in range(0, 65535+1, fade_step):
            led_fading.duty_u16(duty_cycle)
            pot_value = pot.read_u16()
            
            # Set duty cycle on 2nd LED
            led_pot.duty_u16(pot_value)
            sleep(0.01)

        # Breathe out: Decrease the duty cycle of the first LED
        for duty_cycle in range(65535, -1, -fade_step):
            led_fading.duty_u16(duty_cycle)
            pot_value = pot.read_u16()
            
            # Set duty cycle on 2nd LED
            led_pot.duty_u16(pot_value)  
            sleep(0.01)
            
        print(f'pot_value = {pot_value}: '
              f'{round((pot_value/65535)*100)}%')
        sleep(1)  # delay between "breaths"

except KeyboardInterrupt:
    print("\nProgram interrupted by user.")

# Turn off PWM on Slice 7   
finally:
    print("Exiting...")
    
    led_fading.duty_u16(0)
    led_pot.duty_u16(0)
    sleep(1)  # allow PWM hardware to settle
    
    led_fading.deinit()
    led_pot.deinit()