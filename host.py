import socket
import time

# Raspberry Pi Network Configuration
HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 8000       # Port number for the server

# Create a socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Bind the socket to the host and port
    server_sock.bind((HOST, PORT))
    server_sock.listen(1)
    print(f"Server listening on {HOST}:{PORT}...")

    # Wait for a client to connect
    conn, addr = server_sock.accept()
    print(f"Connection established with {addr}")

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
            conn.sendall(message.encode())
            print(f"Sent: {message.strip()}")

        except ValueError:
            print("Invalid input. Please enter coordinates as 'X,Y'")

        time.sleep(1)

except OSError as e:
    print(f"Socket error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
    server_sock.close()
    print("Server shut down.")

--
Canon Ellis | Upper School Computer Science Instructor
St. Stephen’s Episcopal School
6500 St. Stephen’s Drive, Austin, Texas 78746
512.327.1213
www.sstx.org
