"""
webserver_Stepper.py
--------
Microdot webserver for querying status of a stepper motor using
  asyncio
  
"""
# ---------------------------------------------------------------

import asyncio, sys
from microdot import Microdot 
import config_stepper, connect_wifi, pico_event

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

@app.get('/api/v0.1/stepper')
async def Stepper(request):
    event_header = pico_event.header()
    stepper_info   = {
                     'MOTOR_COILS': config_stepper.MOTOR_COILS,
                     'stepping_mode': \
                      config_stepper.stepping_mode,
                     'steps_per_revolution': \
                      config_stepper.steps_per_revolution,
                     'step_sequence': \
                      config_stepper.step_sequence,
                     'step_delay_ms': \
                      config_stepper.step_delay_ms                    
                     }
    event_body     = {
                     'hardware_parameters': \
                     pico_event.hardware_parameters(),
                     'stepper_info': stepper_info
                     }
    return {"header": event_header, "body": event_body}

@app.get('/api/v0.1/stepper/test')
async def Stepper(request):
    event_header = pico_event.header()
    test_info    = {
                     'test_run': config_stepper.test_run,
                     'angle_increments': \
                      config_stepper.angle_increments,
                     'steps_taken': config_stepper.steps_taken,
                     'test_time_elapsed_s': \
                      config_stepper.test_time_elapsed_s,
                     'total_time_elapsed_s': \
                      config_stepper.total_time_elapsed_s
                    }
    event_body   = {
                     'hardware_parameters': \
                      pico_event.hardware_parameters(),
                     'test_info': test_info
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