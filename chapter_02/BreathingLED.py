# BreathingLED.py - Show two LEDs in the same PWM slice using
#   different duty cycles
# ---------------------------------------------------------------

from machine import Pin, PWM
from time import sleep

# Set up PWM Slice 7 on GPIO14 and GPIO15, LED brightness
#   at half max (50% = 32768) for both
led_fading   = PWM(Pin(14), freq=1000, duty_u16=32768)
led_constant = PWM(Pin(15), freq=1000, duty_u16=32768)           

# Vary the brightness level of one LED but keep 
#   the second LED at the same brightness level
try:
    fade_step = 255  
    while True:
        # Breathe in: Increase the duty cycle of the first
        #   LED to 100% brightness (65535)
        for duty_cycle in range(0, 65535+1, fade_step):
            led_fading.duty_u16(duty_cycle)
            sleep(0.01)

        # Breathe out: Decrease the duty cycle of the LED
        for duty_cycle in range(65535, -1, -fade_step):
            led_fading.duty_u16(duty_cycle)
            sleep(0.01)

#         print(f"led_constant PWM duty cycle = "
#               f"{led_constant.duty_u16()}")
        sleep(1)  # Delay between "breaths"

except KeyboardInterrupt:
    print("\nProgram interrupted by user.")

# Turn off PWM on Slice 7         
finally:
    print("Exiting...")
    
    led_fading.duty_u16(0)
    led_constant.duty_u16(0)
    sleep(1)  # allow PWM hardware time to settle

    led_fading.deinit()
    led_constant.deinit()