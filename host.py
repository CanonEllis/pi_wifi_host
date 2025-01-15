import wifi
import socketpool
import time

# Define the Access Point (AP) SSID and password
SSID = "RPI5-AP"  # Replace with your desired SSID
PASSWORD = "12345678"  # Replace with your desired password

# Start Wi-Fi in Access Point mode
wifi.radio.start_ap(ssid=SSID, password=PASSWORD)
print(f"Access Point started with SSID: {SSID}, IP: {wifi.radio.ipv4_address_ap}")

# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)
server_sock = pool.socket(pool.AF_INET, pool.SOCK_STREAM)

# Bind and listen on a port
PORT = 8000
server_sock.bind(("0.0.0.0", PORT))
server_sock.listen(1)
print(f"Listening for connections on port {PORT}...")

try:
    # Wait for a client to connect
    conn, addr = server_sock.accept()
    print(f"Connection from {addr}")

    while True:
        # Get user input for X, Y coordinates
        user_input = input("Enter X,Y coordinates (or type 'close' to end): ").strip()

        if user_input.lower() == "close":
            print("Closing connection...")
            break

        try:
            # Parse and validate input
            x_str, y_str = user_input.split(",")
            x = int(x_str.strip())
            y = int(y_str.strip())

            # Ensure X and Y are within the expected range
            x = max(-255, min(255, x))
            y = max(-255, min(255, y))

            # Send X, Y coordinates to the client
            message = f"{x},{y}\n"
            conn.send(message.encode())
            print(f"Sent: {message.strip()}")

        except ValueError:
            print("Invalid input. Please enter coordinates as 'X,Y'")

        time.sleep(1)

except OSError as e:
    print(f"Socket error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
    print("Connection closed.")
