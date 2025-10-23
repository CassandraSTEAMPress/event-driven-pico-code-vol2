"""
pico_event.py
--------
To obtain a unique event header for the Pico,
  use the ``header()`` function
To obtain hardware parameters for the Pico,
  use the ``hardware_parameters()`` function

Examples::
        >>> import pico_event
        >>> pico_event.header()
        >>> pico_event.hardware_parameters()
"""
import gc
from machine import unique_id, ADC
from os import urandom, statvfs
from time import time, localtime

# Get the serial number of the Pico's flash
machine_unique_id = unique_id().hex()

# Define the version of this event
EVENT_VERSION = "1.0.0"

def header():
    """Get event header
    
    :return: event header for the Pico
    :rtype: dictionary
    """
    # Get a unique id for this event
    event_id = uuid4()
    
    # Get the time for this event
    time_unix  = time() # Unix epoch time
    time_local = "%4d/%02d/%02d %02d:%02d:%02d" \
                 % localtime(time_unix)[:6]
    
    # Define the event header
    event_header = {
                     "machine_unique_id": machine_unique_id,
                     "time_unix":         time_unix,
                     "time_local":        time_local,
                     "event_id":          event_id,
                     "event_version":     EVENT_VERSION,
                   }            

    return event_header

"""Generate a version 4 UUID compliant to RFC 4122"""
def uuid4():
    random_x = bytearray(urandom(16))
    random_x[6] = (random_x[6] & 0x0F) | 0x40
    random_x[8] = (random_x[8] & 0x3F) | 0x80
    h = random_x.hex()
    return str('-'.join((h[0:8], h[8:12], \
                         h[12:16], h[16:20], h[20:32])))

# Set up ADC internal temperature reading
temperature_sensor = ADC(ADC.CORE_TEMP)
conversion_factor = 3.3 / (65535)

def hardware_parameters():
    """Get hardware parameters for the Pico
    
    :return: hardware info about the Pico
    :rtype: dictionary
    """
    # Get the core temperature of the microcontroller
    temp_reading = temperature_sensor.read_u16() \
                   * conversion_factor
    temp_celsius = 27 - (temp_reading - 0.706)/0.001721
    temp_celsius = "{:,.1f} C".format(temp_celsius)

    # Get flash memory size and storage consumption
    flash_status = statvfs("/")
    flash_size = flash_status[1] * flash_status[2]
    flash_free = flash_status[0] * flash_status[3]
    flash_used = flash_size - flash_free
        
    # Get the number of bytes of available heap RAM
    gc.collect()
    free_memory = gc.mem_free()

    hw_params = {
          "temp_celsius": temp_celsius,
          "flash_size":   flash_size,
          "flash_used":   flash_used,
          "flash_free":   flash_free,
          "free_memory":  free_memory
        }
    
    return hw_params