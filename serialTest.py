import serial
import time

PORT = "/dev/ttyS0"    
BAUDRATE = 115200     
TIMEOUT = 1       
RECONNECT_DELAY = 1

def open_serial():
    """Coba buka koneksi serial dan kembalikan objek serial."""
    while True:
        try:
            ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
            print(f"[INFO] Serial port {PORT} opened with baudrate {BAUDRATE}")
            return ser
        except serial.SerialException as e:
            print(f"[ERROR] Failed to open serial port: {e}")
            print(f"[INFO] Reconnecting in {RECONNECT_DELAY} seconds...")
            time.sleep(RECONNECT_DELAY)

def main():
    ser = None
    try:
        ser = open_serial()

        while True:
            try:
                # Baca data jika tersedia
                data = ser.read(ser.in_waiting or 1)
                if data:
                    hex_data = ' '.join(f'{b:02X}' for b in data)
                    print(f"[HEX] {hex_data}")
                time.sleep(0.01)

            except serial.SerialException as e:
                print(f"[ERROR] Serial error: {e}")
                print("[INFO] Attempting to reconnect...")
                try:
                    if ser and ser.is_open:
                        ser.close()
                        print("[INFO] Closed previous serial connection.")
                except:
                    pass
                ser = open_serial()  # Coba buka ulang

    except KeyboardInterrupt:
        print("\n[INFO] Program interrupted by user.")
    finally:
        if ser and ser.is_open:
            ser.close()
            print(f"[INFO] Serial port {PORT} closed.")

if __name__ == "__main__":
    main()
