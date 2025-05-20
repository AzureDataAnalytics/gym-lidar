import pigpio

class DualServoController:
    def __init__(self, pin_Pitch, pin_Yaw):
        # Initialize the servo controller with the specified GPIO pins for pitch and yaw
        self.pin_Pitch = pin_Pitch
        self.pin_Yaw = pin_Yaw

        self.pi = pigpio.pi()  # Connect to the pigpio daemon
        if not self.pi.connected:
            # Raise an error if the pigpio daemon is not running
            raise IOError("Unable to connect to pigpio daemon. Ensure 'sudo pigpiod' is running.")

        # Set the GPIO pins to output mode (optional, pigpio sets this automatically)
        self.pi.set_mode(self.pin_Pitch, pigpio.OUTPUT)
        self.pi.set_mode(self.pin_Yaw, pigpio.OUTPUT)

    def setServo(self, pulseWidthPitch, pulseWidthYaw):
        # Set the servo pulse width in microseconds (typically between 500–2500 µs)
        self.pi.set_servo_pulsewidth(self.pin_Pitch, pulseWidthPitch)
        self.pi.set_servo_pulsewidth(self.pin_Yaw, pulseWidthYaw)

    def cleanup(self):
        # Stop the PWM signal by sending a pulse width of 0
        self.pi.set_servo_pulsewidth(self.pin_Pitch, 0)
        self.pi.set_servo_pulsewidth(self.pin_Yaw, 0)
        self.pi.stop()  # Disconnect from the pigpio daemon
