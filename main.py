import time
import random
import threading
import servoController
import TFLidarReader
from collections import deque

# Configuration
PORT = "/dev/ttyS0"  # Serial port for the LiDAR sensor
BAUDRATE = 115200  # Baud rate for serial communication

SERVO_MOVING_TIME = 0.7  # Time in seconds for servo movement delay
FILTER_WINDOW = 10  # Size of the median filter window
LOWER = 1  # Lower threshold for triggering servo movement (in cm)
UPPER = 10  # Upper threshold for triggering servo movement (in cm)
LOOP_TIME = 0.1  # Delay for main loop (in seconds)
LIDAR_LOOP_TIME = 0.01  # Delay between LiDAR readings in the thread (in seconds)

# PWM limits for servo movement
PWM_LIMITS = {
    "pitch": (1700, 1850),  # PWM range for pitch servo
    "yaw": (1000, 2000),  # PWM range for yaw servo
}

# Shared state for LiDAR data
state = {
    "distance": None,  # Filtered distance from LiDAR
    "strength": None,  # Signal strength from LiDAR
    "temperature": None  # Temperature from LiDAR
}
lock = threading.Lock()  # Lock for thread-safe access to shared state

# Initialize the servo controller
servo = servoController.DualServoController(pin_Pitch=19, pin_Yaw=18)

def median(values):
    """Calculate the median of a list of values."""
    values = sorted(values)  # Sort the values
    n = len(values)
    if n % 2 == 1:
        return values[n // 2]  # Return the middle value for odd-length lists
    else:
        # Return the average of the two middle values for even-length lists
        return (values[n // 2 - 1] + values[n // 2]) / 2

def read_lidar():
    """Thread to read data from the LiDAR sensor with a median filter."""
    lidar = TFLidarReader.BenewakeLidar(PORT, BAUDRATE)  # Initialize the LiDAR sensor
    distance_window = deque(maxlen=FILTER_WINDOW)  # Sliding window for median filter

    while True:
        try:
            # Read distance, signal strength, and temperature from the LiDAR sensor
            distance, strength, temperature = lidar.get_reading()
            
            # Apply the median filter if the window is full, otherwise use the raw distance
            if len(distance_window) == FILTER_WINDOW:
                filtered_distance = median(distance_window)
            else:
                filtered_distance = distance  # Not enough data for filtering yet
            
            # Update the shared state with the filtered distance and other sensor data
            with lock:
                state.update({
                    "distance": filtered_distance,
                    "strength": strength,
                    "temperature": temperature
                })
        except Exception as e:
            # Handle any errors that occur during LiDAR data reading
            print(f"[LIDAR ERROR] {e}")
        
        # Wait for the next reading based on the LiDAR loop time
        time.sleep(LIDAR_LOOP_TIME)

def move_servo():
    """Move the servo to random positions within the defined PWM limits."""
    pitch_pwm = random.randint(*PWM_LIMITS["pitch"])  # Random PWM for pitch
    yaw_pwm = random.randint(*PWM_LIMITS["yaw"])  # Random PWM for yaw
    servo.setServo(pitch_pwm, yaw_pwm)  # Set the servo to the new position
    print(f"[SERVO] Pitch: {pitch_pwm}, Yaw: {yaw_pwm}")

def is_triggered(current, baseline):
    """Check if the change in distance is significant enough to trigger the servo."""
    delta = abs(current - baseline)  # Calculate the change in distance
    return LOWER < delta < UPPER  # Return True if the change is within the defined range

def main():
    # Start the LiDAR reading thread
    threading.Thread(target=read_lidar, daemon=True).start()

    baseline = None  # Baseline distance for comparison
    last_servo_time = 0  # Timestamp of the last servo movement
    servo_active = False  # Flag to indicate if the servo is currently active

    while True:
        # Safely access the shared state
        with lock:
            distance = state["distance"]
            strength = state["strength"]
            temperature = state["temperature"]

        if distance is None:
            # Wait for LiDAR data to become available
            print("[INFO] Waiting for LiDAR data...")
            time.sleep(0.1)
            continue

        if baseline is None:
            # Set the initial baseline distance
            baseline = distance

        current_time = time.time()  # Get the current time
        delta = abs(distance - baseline)  # Calculate the change in distance

        if servo_active and (current_time - last_servo_time >= SERVO_MOVING_TIME):
            # Reset the baseline and deactivate the servo after the movement delay
            baseline = distance
            servo_active = False
            print("[INFO] Start Reading for LiDAR data...")
        
        if not servo_active and is_triggered(distance, baseline):
            # Trigger the servo if the change in distance is significant
            threading.Thread(target=move_servo, daemon=True).start()
            last_servo_time = current_time  # Update the last servo movement time
            servo_active = True  # Mark the servo as active

        # Print the current LiDAR data
        print(f"[DATA] Distance: {distance:.1f} cm | Baseline: {baseline:.1f} cm | Δ: {delta:.1f} cm | Strength: {strength} | Temp: {temperature:.2f}°C")
        time.sleep(LOOP_TIME)  # Wait for the next loop iteration

if __name__ == "__main__":
    main()  # Run the main function
