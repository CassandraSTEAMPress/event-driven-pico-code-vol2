# stepper_HalfStepMode.py - Move 28BYJ-48 Stepper Motor in
#   half-step mode 
# ---------------------------------------------------------------

from machine import Pin
from time import sleep, sleep_ms, ticks_ms, ticks_diff

# Define GPIO pins connected to the input pins (IN1-IN4) of the
#   ULN2003 Motor Driver
coil_A = Pin(21, Pin.OUT)  # GPIO21
coil_B = Pin(20, Pin.OUT)
coil_C = Pin(19, Pin.OUT)
coil_D = Pin(18, Pin.OUT)
MOTOR_COILS = [coil_A, coil_B, coil_C, coil_D]

# Define half-step sequence
SEQUENCE_HALF_STEPS = [
    [1, 0, 0, 0], # Step 0: Coil A ON     | Blue
    [1, 1, 0, 0], # Step 1: Coil A & B ON | Blue & Pink
    [0, 1, 0, 0], # Step 2: Coil B ON     | Pink
    [0, 1, 1, 0], # Step 3: Coil B & C ON | Pink & Yellow
    [0, 0, 1, 0], # Step 4: Coil C ON     | Yellow
    [0, 0, 1, 1], # Step 5: Coil C & D ON | Yellow & Orange
    [0, 0, 0, 1], # Step 6: Coil D ON     | Orange
    [1, 0, 0, 1]  # Step 7: Coil D & A ON | Orange & Blue
]

# Number of steps per output shaft rotation
HALF_STEPS_PER_REVOLUTION = 4096

# Minimum and maximum delays between steps
MIN_DELAY = 1
MAX_DELAY = 20

# Initialize the current step sequence
step_sequence = SEQUENCE_HALF_STEPS
len_step_sequence = len(step_sequence)
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
                                 #  (typically 1ms-5ms)

        # Direction is forward (clockwise)
        if steps >= 0:
            # Increment step sequence index, wrapping around to
            #   the beginning of the sequence if it exceeds the
            #   sequence length
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
        coil.value(0)  # turn off motor coil

# Convert degrees to step increments
def degrees_to_steps(degrees):
    if abs(degrees) > 360:
        raise ValueError("Degrees should be between "
                         "-360 and 360")
    steps = int(degrees / 360 * HALF_STEPS_PER_REVOLUTION)
    return (steps)

# Test moving the motor at various angles in half-step mode
def test_stepper_motor():
 
    # Define angle increments
    angle_increments = [30, 1.8, 7.5, 0.9, 15, 45, 135, 22.5]

    # Run motor test
    print(f"28BYJ-48 Half-Step Motor Test")
    print(f"=============================")

    test_runs = 3
    test_time_elapsed_s = ""
    total_time_elapsed_ms = 0
    total_time_elapsed_s = ""
    for test_run in range(test_runs): 
        print(f"\nTest Run: {test_run+1}")
        test_run = test_run + 1

        # Start timer
        t_start = ticks_ms()

        # Rotate motor
        steps_taken = 0
        for angle in angle_increments:
            steps_taken = steps_taken + step_motor(\
                degrees_to_steps(angle), step_delay_ms=5)
            sleep(0.1)  # pause between angle positions

        print(f"Test Motor: steps_taken (forward) = "
              f"{steps_taken}")

        # Return to starting position
        step_motor(-steps_taken, step_delay_ms=5)
        sleep(1)  # pause after returning to starting position

        # Stop timer
        t_end = ticks_ms()
        t_elapsed_ms = ticks_diff(t_end, t_start)
        total_time_elapsed_ms \
                        = total_time_elapsed_ms + t_elapsed_ms

        # Convert ms to seconds
        test_time_elapsed_s = f"{t_elapsed_ms / 1000:.2f} "\
                              f"seconds"
        print(f"Test time elapsed = {test_time_elapsed_s}")
        
        total_time_elapsed_s \
                    = f"{total_time_elapsed_ms/1000:.2f} seconds"
        print(f"Total Elapsed Time = "
              f"{total_time_elapsed_ms/1000:.2f} seconds")
        
    print(f"\n\n>>> End of Tests: Total Elapsed Time = " \
          f"{total_time_elapsed_s} <<<")

if __name__ == "__main__":
    # Pico onboard LED
    pico_led = Pin("LED", Pin.OUT)

    # Turn on Pico onboard LED
    pico_led.on()
    
    try:
        # Run motor test
        test_stepper_motor()
        
    # Keyboard interrupt caught
    except KeyboardInterrupt:
        print("\nUser interrupted the program")
        
    # Unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Stop the motor gracefully
    finally:
        # Turn off the motor
        stop_motor()

        print("\nMotor control terminated.")

    # Turn off Pico onboard LED
    pico_led.off()