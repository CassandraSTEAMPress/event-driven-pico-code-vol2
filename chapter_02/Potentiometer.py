# Potentiometer.py - Use ADC (analog to digital) to convert an
#   output voltage from a potentiometer (range 0.0v - 3.3v) to a
#   digital reading
# ---------------------------------------------------------------

from machine import Pin, ADC
from time import sleep

# Use GPIO28 to read analog output voltage from a potentiometer
pot = ADC(Pin(28))

# Display potentiometer reading
try:
    while True:
        pot_value = pot.read_u16() 
        print(f'pot_value = {round((pot_value/65535)*100)}%')
        sleep(1)  # delay between readings
  
# Catch keyboard interrupt         
except KeyboardInterrupt:
    print("\nProgram interrupted by user.")

finally:
    print("Exiting...")