import serial

# Constants for Benewake LiDAR
BENEWAKE_FRAME_HEADER = 0x59  # Frame header byte for Benewake LiDAR
BENEWAKE_FRAME_LENGTH = 9  # Length of a valid data frame
BENEWAKE_DIST_MAX_CM = 600  # Maximum measurable distance in cm
BENEWAKE_OUT_OF_RANGE_ADD_CM = 100  # Additional value for out-of-range readings

class BenewakeLidar:
    def __init__(self, port, baudrate):
        # Initialize the serial connection with the specified port and baud rate
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.buffer = bytearray()  # Buffer to store incoming data

    def get_reading(self):
        # Variables to calculate the average distance and handle out-of-range readings
        sum_cm = 0  # Sum of valid distances
        count = 0  # Count of valid distance readings
        count_out_of_range = 0  # Count of out-of-range readings
        strength = None  # Signal strength
        temperature = None  # Temperature in Celsius

        while self.ser.in_waiting:  # Check if there is data available in the serial buffer
            c = self.ser.read(1)[0]  # Read one byte from the serial buffer
            # Frame Header Check
            if len(self.buffer) == 0:
                # Start a new frame if the first byte matches the frame header
                if c == BENEWAKE_FRAME_HEADER:
                    self.buffer.append(c)
            elif len(self.buffer) == 1:
                # Add the second frame header byte if it matches
                if c == BENEWAKE_FRAME_HEADER:
                    self.buffer.append(c)
                else:
                    # Clear the buffer if the second byte is invalid
                    self.buffer.clear()
            else:
                # Append the byte to the buffer
                self.buffer.append(c)
                if len(self.buffer) == BENEWAKE_FRAME_LENGTH:
                    # Checksum verification
                    checksum = sum(self.buffer[:-1]) & 0xFF  # Calculate checksum
                    if checksum == self.buffer[-1]:  # Verify checksum
                        # Extract distance, strength, and temperature from the frame
                        dist = (self.buffer[3] << 8) | self.buffer[2]  # Distance in cm
                        strength = (self.buffer[5] << 8) | self.buffer[4]  # Signal strength
                        raw_temp = (self.buffer[7] << 8) | self.buffer[6]  # Raw temperature
                        temperature = (raw_temp / 8.0) - 256.0  # Convert raw temperature to Celsius

                        if dist >= BENEWAKE_DIST_MAX_CM:
                            # Increment out-of-range count if distance exceeds the maximum
                            count_out_of_range += 1
                        else:
                            # Add valid distance to the sum and increment the count
                            sum_cm += dist
                            count += 1
                    # Clear the buffer after processing the frame
                    self.buffer.clear()
        
        if count > 0:
            # Return the average distance, signal strength, and temperature if valid readings exist
            return sum_cm / count, strength, temperature
        if count_out_of_range > 0:
            # Return the maximum distance and additional value for out-of-range readings
            return max(BENEWAKE_DIST_MAX_CM, BENEWAKE_OUT_OF_RANGE_ADD_CM), strength, temperature
        
        # Return None if no valid readings are available
        return None, None, None
