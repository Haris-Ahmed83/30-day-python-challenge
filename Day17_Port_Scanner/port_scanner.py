
import socket
import argparse
import concurrent.futures

def scan_port(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                    return f"Port {port} is open (Service: {service})"
                except OSError:
                    return f"Port {port} is open (Service: Unknown)"
            else:
                return None
    except socket.error as e:
        return f"Error scanning port {port}: {e}"

def main():
    parser = argparse.ArgumentParser(description="Simple TCP Port Scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Port range to scan (e.g., '1-100', '80,443', '22')")
    parser.add_argument("-t", "--timeout", type=float, default=1,
                        help="Connection timeout in seconds (default: 1)")
    parser.add_argument("-w", "--workers", type=int, default=10,
                        help="Number of concurrent workers (default: 10)")

    args = parser.parse_args()

    target_ip = socket.gethostbyname(args.target)
    print(f"Scanning target: {args.target} ({target_ip})")

    ports_to_scan = []
    for part in args.ports.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports_to_scan.extend(range(start, end + 1))
        else:
            ports_to_scan.append(int(part))

    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_port = {executor.submit(scan_port, target_ip, port, args.timeout): port for port in ports_to_scan}
        for future in concurrent.futures.as_completed(future_to_port):
            result = future.result()
            if result:
                open_ports.append(result)

    if open_ports:
        print("\nOpen ports found:")
        for port_info in open_ports:
            print(port_info)
    else:
        print("\nNo open ports found in the specified range.")

if __name__ == "__main__":
    main()
