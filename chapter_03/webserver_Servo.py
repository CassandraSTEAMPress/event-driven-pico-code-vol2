"""
webserver_Servo.py
--------
Microdot webserver for querying the status of a servomotor using
  asyncio
"""
# ---------------------------------------------------------------

import asyncio, sys
from microdot import Microdot 
import config_servo, connect_wifi, pico_event

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

@app.get('/api/v0.1/servo')
async def Servo(request):
    event_header = pico_event.header()
    servo_info   = {
                     'pin_id': config_servo.pin_id,
                     'min_us': config_servo.min_us,
                     'max_us': config_servo.max_us,
                     'min_deg': config_servo.min_deg,
                     'max_deg': config_servo.max_deg,
                     'freq': config_servo.freq
                   }
    event_body   = {
                     'hardware_parameters': \
                      pico_event.hardware_parameters(),
                     'servo_info': servo_info
                   }
    return {"header": event_header, "body": event_body}

@app.get('/api/v0.1/servo/angle')
async def Servo(request):
    event_header = pico_event.header()
    event_body   = {
                     'servo_angle': config_servo.servo_angle
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