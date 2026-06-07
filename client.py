import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    """Connect to the TCP server and allow the user to send messages."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"[CLIENT] Connecting to {HOST}:{PORT}...")
        client_socket.connect((HOST, PORT))
        print("[CLIENT] Connected successfully.")

        while True:
            message = input("Enter message for server (type 'bye' to quit): ").strip()

            if not message:
                print("[CLIENT] Empty message not sent.")
                continue

            client_socket.sendall(message.encode("utf-8"))
            print(f"[CLIENT] Sent: {message}")

            response = client_socket.recv(1024).decode("utf-8")
            print(f"[CLIENT] Received: {response}")

            if message.lower() == "bye":
                print("[CLIENT] Closing connection gracefully.")
                break

    except ConnectionRefusedError:
        print("[CLIENT] Error: Server is not running or refused the connection.")
    except socket.gaierror:
        print("[CLIENT] Error: Invalid address or hostname.")
    except Exception as error:
        print(f"[CLIENT] Unexpected error: {error}")
    finally:
        client_socket.close()
        print("[CLIENT] Client socket closed.")

if __name__ == "__main__":
    main()

