# HOW TO RUN 
## 1. Enable pigpio
```
./enable_pigpio.sh
```
## 2. run main.py
```
python3 main.py
```
# PARAMETERS (main.py)
## 1. Serial Port & Baudrate LiDAR
```
PORT = "/dev/ttyS0"
BAUDRATE = 115200
```
## 2. Trigger Servo
Time in seconds for servo movement delay
```
SERVO_MOVING_TIME = 0.7
```
Lower threshold for triggering servo movement (in cm)
```
LOWER = 1
```
Upper threshold for triggering servo movement (in cm)
```
UPPER = 10
```
## 3. Filter Data
Size of the median filter window
```
FILTER_WINDOW = 10
```
## 4. Loop Delay
Delay for main loop (in seconds)
```
LOOP_TIME = 0.1
```
Delay between LiDAR readings in the thread (in seconds)
```
LIDAR_LOOP_TIME = 0.01
```
## 5. PWM Servo Limiter
```
PWM_LIMITS = {
    "pitch": (1700, 1850),  # (min,max)
    "yaw": (1000, 2000),  # (min,max)
}
```
