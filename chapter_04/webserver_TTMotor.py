"""
webserver_TTMotor.py
--------
Microdot webserver for querying status of a TT motor using
  asyncio
"""
# ---------------------------------------------------------------

import asyncio, sys
from microdot import Microdot 
import config_ttmotor, connect_wifi, pico_event

# Add my_secrets.py to the .gitignore file to make sure
#   that my_secrets.py is never checked into GitHub 
import my_secrets
ssid = my_secrets.SSID          # Your SSID (Network Name)
password = my_secrets.PASSWORD  # Your WiFi PASSWORD

# Initialize the WiFi Interface
if not connect_wifi.init_wlan(ssid, password, max_retries=10):
    print('WiFi authentication error: {connect_wifi.SSID_ERROR}')
    print('Exiting program')
    sys.exit(0)
else:
    ip_address = connect_wifi.get_ip()

# Instantiate a Microdot webserver
app = Microdot()

# Microdot communications interface
@app.get('/api/v0.1/hello')
async def hello(request):
    event_header = pico_event.header()
    event_body   = {'greeting': 'Hello, world!'}
    return {"header": event_header, "body": event_body}

@app.get('/api/v0.1/ttmotor')
async def TTMotor(request):
    event_header = pico_event.header()
    ttmotor_info = {
                    'motorA_IN1': config_ttmotor.motorA_IN1,
                    'motorA_IN2': config_ttmotor.motorA_IN2,
                    'motorA_freq': config_ttmotor.motorA_freq
                   }
    event_body   = {
                     'hardware_parameters': \
                      pico_event.hardware_parameters(),
                     'ttmotor_info': ttmotor_info
                   }
    return {"header": event_header, "body": event_body}

@app.get('/api/v0.1/ttmotor/speed')
async def TTMotor(request):
    event_header = pico_event.header()
    event_body   = {
                     'motorA_decay_mode': \
                      config_ttmotor.motorA_decay_mode,
                     'motorA_direction': \
                      config_ttmotor.motorA_direction,
                     'motorA_speed': config_ttmotor.motorA_speed
                   }
    return {"header": event_header, "body": event_body}

async def start_server():
    try:
        # Run the Microdot webserver
        print('Starting Microdot webserver ...')
        await app.start_server(host=ip_address, port=80,
                               debug=True)
        
    # Keyboard interrupt caught
    except KeyboardInterrupt:
        print("\nUser interrupted the program")
        
    # Unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # End the program gracefully
    finally:
        print("\nMicrodot server stopped.")
        app.shutdown()