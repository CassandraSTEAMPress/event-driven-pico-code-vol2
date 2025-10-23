# TTMotor_VariableSpeed.py - Rotate a TT Motor at different
#   speeds using the DRV8833
# ---------------------------------------------------------------

from machine import Pin, PWM
from time import sleep

# Specify the Pico W pins connected to the motor driver
motorA_IN1 = Pin(14, Pin.OUT)  # GPIO14
motorA_IN1.value(0)

motorA_IN2 = Pin(15, Pin.OUT)  # GPIO15
motorA_IN2.value(0)

# Create a PWM instance for controlling the motor's speed
#   using a PWM Frequency = 50Hz
motorA_IN1_PWM = PWM(motorA_IN1, freq=50)
motorA_IN1_PWM.duty_u16(0)

# Direction and decay mode (informational)
motorA_direction = "Forward"
motorA_decay_mode = "FAST DECAY"

# Stop the motor
def stop_motor():
    print("Stopping motor")
    motorA_IN1.value(0)  
    motorA_IN2.value(0)  
    motorA_IN1_PWM.duty_u16(0)
    sleep(1)  # allow PWM hardware time to settle

    # Turn off PWM
    motorA_IN1_PWM.deinit()
        
# Rotate the motor forward at different speeds  
def TTMotor_variable_speed():

    # 40% Speed: 26214/65535
    speed_u16=26214  
    motorA_IN1_PWM.duty_u16(speed_u16)
    print(f"Motor speed: {speed_u16/65535*100:.2f}%")
    sleep(2)

    # 60% Speed: 39321/65535
    speed_u16=39321
    motorA_IN1_PWM.duty_u16(speed_u16)
    print(f"Motor speed: {speed_u16/65535*100:.2f}%")
    sleep(2)

    # 80% Speed: 52428/65535
    speed_u16=52428
    motorA_IN1_PWM.duty_u16(speed_u16)
    print(f"Motor speed: {speed_u16/65535*100:.2f}%")
    sleep(2)

    # 100% Speed: 65535/65535
    speed_u16=65535
    motorA_IN1_PWM.duty_u16(65535)
    print(f"Motor speed: {speed_u16/65535*100:.2f}%")
    sleep(2)

if __name__ == "__main__":
    
    # Run motor test
    try:
        for i in range(5):
            print(f"\nTest: {i+1}")
            print(f"=======")
            TTMotor_variable_speed()

        print("\n\n>>> End of Tests <<<")      

    # Keyboard interrupt caught        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

    # Unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Stop the motor
    finally:   
        # Turn off the motor
        stop_motor()
        
        print("\nMotor control terminated.")