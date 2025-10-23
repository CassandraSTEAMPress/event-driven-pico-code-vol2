# stepper_Interactive.py - Interactively set the speed and 
#   direction of the 28BYJ-48 Stepper Motor in full-step mode
# ---------------------------------------------------------------

from machine import Pin
from time import sleep, sleep_ms

# Define GPIO pins connected to the input pins (IN1-IN4) of the
#   ULN2003 Motor Driver
coil_A = Pin(21, Pin.OUT)  # GPIO21
coil_B = Pin(20, Pin.OUT)
coil_C = Pin(19, Pin.OUT)
coil_D = Pin(18, Pin.OUT)
MOTOR_COILS = [coil_A, coil_B, coil_C, coil_D]

# Define single phase ON sequence
SEQUENCE_SINGLE_PHASE = [
    [1, 0, 0, 0], # Step 0: Coil A ON | Blue
    [0, 1, 0, 0], # Step 1: Coil B ON | Pink
    [0, 0, 1, 0], # Step 2: Coil C ON | Yellow
    [0, 0, 0, 1], # Step 3: Coil D ON | Orange
]

# Define two phase ON sequence
SEQUENCE_TWO_PHASE = [
    [1, 1, 0, 0], # Step 1: Coil A & B ON | Blue & Pink
    [0, 1, 1, 0], # Step 3: Coil B & C ON | Pink & Yellow
    [0, 0, 1, 1], # Step 5: Coil C & D ON | Yellow & Orange
    [1, 0, 0, 1]  # Step 7: Coil D & A ON | Orange & Blue
]
    
# Number of steps per output shaft rotation
FULL_STEPS_PER_REVOLUTION = 2048

# Minimum and maximum delays between steps
MIN_DELAY = 1
MAX_DELAY = 20

# Initialize the current step sequence
step_sequence = SEQUENCE_SINGLE_PHASE
len_step_sequence = len(SEQUENCE_SINGLE_PHASE)
pos_step_sequence = 0  # starting step in the sequence 

# Rotate the motor by a number of steps in a given
#   direction: "+" = forward; "-" = backward
def step_motor(steps=0, step_delay_ms=5):
    if (step_delay_ms < MIN_DELAY or step_delay_ms > MAX_DELAY):
        raise ValueError(f"step_delay_ms should be an integer "
                         f"between {MIN_DELAY} and {MAX_DELAY}.")
        return
    global pos_step_sequence
    
    for _ in range(abs(steps)):
        
        # Set the state of each motor coil for the step in the
        #   sequence
        step = step_sequence[pos_step_sequence]
        for i, pin_val in enumerate(step):
            MOTOR_COILS[i].value(pin_val) 
        sleep_ms(step_delay_ms)  # delay between steps
                                 #   (typically 1ms-5ms)

        # Direction is forward (clockwise)
        if steps >= 0:
            # Increment step sequence index, wrapping around to
            #   the beginning of the sequence if it exceeds the
            #    sequence length
            pos_step_sequence = (pos_step_sequence + 1) \
                                % len_step_sequence
        # Direction is backward (counter-clockwise)
        else: 
            # Decrement the step sequence index
            pos_step_sequence = (pos_step_sequence - 1) \
                                % len_step_sequence
            # Wrap around to the end of the sequence if the
            #   index < 0
            if pos_step_sequence < 0: 
                pos_step_sequence = len_step_sequence - 1

    return steps

# Stop the motor by turning off all the motor coils
def stop_motor():
    print("Stopping motor")
    for coil in MOTOR_COILS:
        coil.value(0) # turn off motor coil

def interactive_control():
    while True:
        # Get steps and delay between steps
        steps = int(input(f"Steps (must be between "
                          f"-{FULL_STEPS_PER_REVOLUTION} and "
                          f"{FULL_STEPS_PER_REVOLUTION}): "))
        step_delay_ms = int(input("Step delay in ms (e.g. 5): "))
        step_motor(steps, step_delay_ms)    

if __name__ == "__main__":
    # Pico onboard LED
    pico_led = Pin("LED", Pin.OUT)

    # Turn on Pico onboard LED
    pico_led.on()
    
    try:
        # Run motor interactively
        interactive_control()
            
    # Keyboard interrupt caught
    except KeyboardInterrupt:
        print("\nUser interrupted the program")
        
    # Unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Stop the motor
    finally:

        # Turn off the motor
        stop_motor()

        print("\nMotor control terminated.")

    # Turn off Pico onboard LED
    pico_led.off()