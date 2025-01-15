#!/usr/bin/env python3

import socket

HOST = ''       # Listen on all interfaces (0.0.0.0)
PORT = 8000     # Same port you used in your ESP32 code

def main():
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Listening on {HOST}:{PORT} ...")

        while True:
            # Wait for a client (ESP32, etc.) to connect
            conn, addr = s.accept()
            print("Connected by", addr)
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        # Connection closed by client
                        print("Client disconnected.")
                        break
                    # Decode/print the data
                    message = data.decode('utf-8').strip()
                    print("Received:", message)

                    # Optionally send a response back
                    response = f"Hello from RPi5! You said: {message}\n"
                    conn.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    main()
