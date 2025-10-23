# PWMExample_VeryBasic.py - Init and deinit PWM on a GPIO pin
# ---------------------------------------------------------------

from machine import Pin, PWM
from time import sleep

# Set up PWM on Slice 7, Channel A (GPIO14)
pwm_7A = PWM(Pin(14), freq=1000, duty_u16=39321)

# Display the properties of the PWM object
print(f"PWM frequency  = {pwm_7A.freq()}")
print(f"PWM duty cycle = {pwm_7A.duty_u16()}")

# Turn off PWM
pwm_7A.duty_u16(0)
sleep(1)  # allow PWM hardware time to settle

pwm_7A.deinit()    