import serial
import time

PORT = "/dev/ttyS0"    
BAUDRATE = 115200     
TIMEOUT = 1       

def main():
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
        print(f"[INFO] Serial port {PORT} opened with baudrate {BAUDRATE}")

        while True:
            data = ser.read(ser.in_waiting or 1)
            if data:
                hex_data = ' '.join(f'{b:02X}' for b in data)
                print(f"[HEX] {hex_data}")
            time.sleep(0.01)

    except serial.SerialException as e:
        print(f"[ERROR] Serial connection failed: {e}")
    except KeyboardInterrupt:
        print("\n[INFO] Program interrupted by user.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print(f"[INFO] Serial port {PORT} closed.")

if __name__ == "__main__":
    main()
