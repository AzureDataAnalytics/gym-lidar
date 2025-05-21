# HOW TO RUN 
## 1. Enable pigpio
```
./enable_pigpio.sh
```
## 2. run main.py
```
python3 main.py
```
# PARAMETERS
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
