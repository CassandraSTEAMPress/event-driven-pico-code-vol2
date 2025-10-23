"""
webserver_PWMLEDs.py
--------
Microdot webserver for querying status of PWM LEDs using asyncio
  
"""
# ---------------------------------------------------------------

import asyncio, sys
from microdot import Microdot
import config_pwm, connect_wifi, pico_event

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

# Create a Microdot instance
app = Microdot()

# MicroDot communications interface
@app.get('/api/v0.1/hello')
async def hello(request):
    event_header = pico_event.header()
    event_body   = {'greeting': 'Hello, world!'}
    return {"header": event_header, "body": event_body}

@app.get('/api/v0.1/PWM')
async def PWMLEDs(request):
    event_header = pico_event.header()
    PWM_info = {
                 'PWM_Slice': config_pwm.PWM_Slice,
                 'PWM_frequency': config_pwm.PWM_frequency,
                 'fade_step': config_pwm.fade_step
               }
    event_body   = {
                     'hardware_parameters': \
                      pico_event.hardware_parameters(),
                     'PWM_info': PWM_info
                   }
    return {"header": event_header, "body": event_body}

@app.get('/api/v0.1/PWM/LEDs')
async def PWMLEDs(request):
    event_header = pico_event.header()
    PWM_info = {
                 'led_fading_duty_cycle': \
                 'breathing (range 0-65535)',
                 'pot_duty_cycle': config_pwm.pot_duty_cycle
               }

    event_body   = {
                     'PWM_info': PWM_info
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