"""
connect_wifi.py
-----------
To connect to a wireless network,
    use the ``init_wlan()`` function
To obtain the IP address, use the ``get_ip()`` function

Example::
        >>> import connect_wifi
        >>> connect_wifi.init_wlan('Your Network Name',    \
                                   'Your Network Password' \
                                   max_retries=23)
        >>> connect_wifi.get_ip()

For information on MicroPython's WLAN built-in WiFi
    interfaces, see:
    docs.micropython.org/en/latest/library/network.WLAN.html
"""
import network
from time import sleep


# Network error messages
NETWORK_CONNECTION_ERROR = "Network connection failed"
SSID_ERROR = "Failed to obtain IP address"

# Create a WLAN network interface object in Station (STA) mode
wlan = network.WLAN(network.STA_IF)

def init_wlan(ssid, password, max_retries=10):
    """Initiate a wireless LAN connnection
    
    :param ssid: wireless network name
    :param password: wireless network password
    :param max_retries: number of connection attempts before
        giving up
    
    :raise RuntimeError: If the network connection failed

    :return: True (successful connection);
             False (unsuccessful connection)
    :rtype: bool
    """

    # Activate network interface
    wlan.active(True)

    # Connect to the specified wireless network, using the 
    #   wireless network name and password
    wlan.connect(ssid, password)

    # Print a message to the console saying that the device 
    #   is trying to connect
    print('Waiting for connection...')
    
    # Continue to loop as long as there are connection attempts
    while max_retries > 0:
        # wlan.status() < 0: connection failure
        # wlan.status() >= 3: connection successful
        #   or has a valid IP address
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        print(max_retries, '.', sep='', end='', )
        max_retries -= 1
        sleep(1)  # delay before retrying
    
    # Check if the connection was unsuccessful 
    if wlan.status() != network.STAT_GOT_IP:   
        raise RuntimeError(NETWORK_CONNECTION_ERROR)
        return False  # unsuccessful connection
    
    # Connection was successful and an IP address was obtained
    else:
        # Get the IP address
        ip = wlan.ifconfig()[0]
        
        # Print a confirmation message to console
        print( 'Connected: ip = {}'.format(ip))  
        return True  # successful connection

def get_ip():
    """Get the IP address if WiFi is connected
    
    :raise RuntimeError: If not connected

    :return: IP Address (successful connection);
             SSID_ERROR (unsuccessful connection)
    :rtype: bool
    """
    if wlan.isconnected():
        return wlan.ifconfig()[0]
    else:
        print('\nNot connected')
        raise RuntimeError(SSID_ERROR)
        return None
        