import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    """Start a basic TCP server that listens for one client at a time."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Lets you restart the server quickly without waiting for the port to fully clear
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"[SERVER] Listening on {HOST}:{PORT}")

        while True:
            print("[SERVER] Waiting for a client connection...")
            client_socket, client_address = server_socket.accept()
            print(f"[SERVER] Connected to {client_address}")

            try:
                while True:
                    data = client_socket.recv(1024)

                    if not data:
                        print("[SERVER] Client disconnected.")
                        break

                    message = data.decode("utf-8").strip()
                    print(f"[SERVER] Received: {message}")

                    if message.lower() == "bye":
                        response = "Goodbye from server."
                        client_socket.sendall(response.encode("utf-8"))
                        print("[SERVER] Closing connection gracefully.")
                        break

                    response = f"Server received: {message}"
                    client_socket.sendall(response.encode("utf-8"))
                    print(f"[SERVER] Sent: {response}")

            except ConnectionResetError:
                print("[SERVER] Connection was reset by the client.")
            except Exception as error:
                print(f"[SERVER] Error while handling client: {error}")
            finally:
                client_socket.close()
                print("[SERVER] Client socket closed.")

    except Exception as error:
        print(f"[SERVER] Fatal error: {error}")
    finally:
        server_socket.close()
        print("[SERVER] Server socket closed.")

if __name__ == "__main__":
    main()
