"""
microdot_PotentiometerBreathingLED.py
--------
Vary the brightness levels of two LEDs in the same PWM slice but
  change the brightness of one of the LEDs with a potentiometer

Use a Microdot webserver to provide data consumers with event
  details
"""
# ---------------------------------------------------------------

from machine import Pin, PWM, ADC
from time import sleep
import asyncio, webserver_PWMLEDs, config_pwm

# Set up PWM on Slice 7 with PWM frequency and same duty cycle
led_fading = PWM(Pin(14), freq=config_pwm.PWM_frequency, \
                 duty_u16=config_pwm.pot_duty_cycle)
led_pot    = PWM(Pin(15), freq=config_pwm.PWM_frequency, \
                 duty_u16=config_pwm.pot_duty_cycle)
sleep(3)  # allow time to observe the brightness levels of
          #   the two LEDs    

"""Vary the brightness level of the first LED but adjust 
     the brightness of the second LED with the potentiometer"""

async def PWM_LEDs(): 
    
    pot = ADC(Pin(28))  # potentiometer
    pot_value = pot.read_u16()
    fade_step = config_pwm.fade_step     

    while True:
        print(f'pot_value = {pot_value}: '
              f'{round((pot_value/65535)*100)}%')
        
        # Breathe in: Increase duty cycle of first LED to 100%
        for duty_cycle in range(0, 65535+1, fade_step):
            led_fading.duty_u16(duty_cycle)
            pot_value = pot.read_u16()
            led_pot.duty_u16(pot_value)  # set duty cycle on
                                         #   2nd LED
            config_pwm.pot_duty_cycle = pot_value
            sleep(0.005)
        await asyncio.sleep_ms(100)  # yield control to the
                                     #   event loop 
        
        # Breathe out: Decrease the duty cycle of the first LED
        for duty_cycle in range(65535, -1, -fade_step):
            led_fading.duty_u16(duty_cycle)
            pot_value = pot.read_u16()
            led_pot.duty_u16(pot_value)  # set duty cycle on
                                         #  2nd LED
            config_pwm.pot_duty_cycle = pot_value
            sleep(0.005)
        await asyncio.sleep_ms(100)  # yield control to the
                                     #   event loop
# Main entry point for the event loop
async def main():
    print("Starting async tasks ...")

    web_server = asyncio.create_task( \
        webserver_PWMLEDs.start_server())
    PWM_LEDs_task = asyncio.create_task(PWM_LEDs())
                                        
    await asyncio.gather(PWM_LEDs_task, web_server)

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

    # Turn off PWM on Slice 7   
    finally:
        print("Exiting...")
        
        led_fading.duty_u16(0)
        led_pot.duty_u16(0)
        sleep(1)  # allow PWM hardware time to settle
    
        led_fading.deinit()
        led_pot.deinit()
        