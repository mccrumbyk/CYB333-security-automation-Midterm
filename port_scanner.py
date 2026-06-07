import socket
import argparse
import time
from datetime import datetime

def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    """Return True if the port is open, otherwise False."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scanner:
            scanner.settimeout(timeout)
            result = scanner.connect_ex((host, port))
            return result == 0
    except socket.gaierror:
        raise ValueError("Hostname could not be resolved.")
    except Exception as error:
        raise RuntimeError(f"Unexpected scanning error: {error}")

def validate_ports(start_port: int, end_port: int) -> None:
    """Validate port range."""
    if start_port < 1 or end_port > 65535:
        raise ValueError("Ports must be between 1 and 65535.")
    if start_port > end_port:
        raise ValueError("Start port cannot be greater than end port.")

def main():
    parser = argparse.ArgumentParser(description="Simple Python Port Scanner")
    parser.add_argument("host", help="Target host (ONLY use 127.0.0.1 or scanme.nmap.org)")
    parser.add_argument("start_port", type=int, help="Start port")
    parser.add_argument("end_port", type=int, help="End port")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between scans in seconds")
    args = parser.parse_args()

    allowed_hosts = ["127.0.0.1", "localhost", "scanme.nmap.org"]

    if args.host not in allowed_hosts:
        print("[ERROR] Unauthorized target. Only use 127.0.0.1, localhost, or scanme.nmap.org.")
        return

    try:
        validate_ports(args.start_port, args.end_port)
    except ValueError as error:
        print(f"[ERROR] {error}")
        return

    print("=" * 50)
    print("Simple Port Scanner")
    print(f"Target: {args.host}")
    print(f"Port range: {args.start_port}-{args.end_port}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    open_ports = []

    try:
        for port in range(args.start_port, args.end_port + 1):
            try:
                if scan_port(args.host, port):
                    print(f"[OPEN] Port {port}")
                    open_ports.append(port)
                else:
                    print(f"[CLOSED] Port {port}")
            except ValueError as error:
                print(f"[ERROR] {error}")
                return
            except RuntimeError as error:
                print(f"[ERROR] {error}")

            time.sleep(args.delay)

    except KeyboardInterrupt:
        print("\n[INFO] Scan interrupted by user.")
        return

    print("\n" + "=" * 50)
    print("Scan complete")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Open ports found: {open_ports if open_ports else 'None'}")
    print("=" * 50)

if __name__ == "__main__":
    main()