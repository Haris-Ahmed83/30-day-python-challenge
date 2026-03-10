# Day 17: Port Scanner

## Project Description

This project implements a multi-threaded TCP port scanner in Python. It allows users to scan a target IP address or hostname for open ports within a specified range. The scanner utilizes `socket` for network communication and `concurrent.futures` for efficient, parallel scanning, making it faster than single-threaded alternatives. It also attempts to identify the service running on open ports.

## Features

- **Multi-threaded Scanning**: Scans multiple ports concurrently using a thread pool.
- **Customizable Port Ranges**: Specify single ports, a range of ports (e.g., `1-100`), or a comma-separated list of ports (e.g., `22,80,443`).
- **Adjustable Timeout**: Configure the connection timeout for each port scan.
- **Service Detection**: Attempts to identify common services running on open ports.
- **Command-Line Interface**: Easy-to-use command-line arguments for target, ports, timeout, and worker threads.

## Installation

This project requires Python 3.6+.

1. **Clone the repository (if you haven't already):**
   ```bash
   git clone https://github.com/Haris-Ahmed83/30-day-python-challenge.git
   cd 30-day-python-challenge/Day17_Port_Scanner
   ```

2. **No external dependencies are required beyond standard Python libraries.**

## Usage

Run the `port_scanner.py` script from your terminal.

```bash
python3 port_scanner.py <target_ip_or_hostname> [options]
```

### Arguments:

- `<target_ip_or_hostname>`: The IP address or hostname of the target to scan.

### Options:

- `-p`, `--ports`: Port range to scan. Examples: `1-1024` (default), `80,443,8080`, `22`. (Default: `1-1024`)
- `-t`, `--timeout`: Connection timeout in seconds. (Default: `1`)
- `-w`, `--workers`: Number of concurrent worker threads. (Default: `10`)

### Examples:

1. **Scan default ports (1-1024) on a target:**
   ```bash
   python3 port_scanner.py scanme.nmap.org
   ```

2. **Scan specific ports (80, 443, 22) on a target:**
   ```bash
   python3 port_scanner.py example.com -p 80,443,22
   ```

3. **Scan a custom range of ports (1-500) with a shorter timeout:**
   ```bash
   python3 port_scanner.py 192.168.1.1 -p 1-500 -t 0.5
   ```

4. **Scan with more concurrent workers:**
   ```bash
   python3 port_scanner.py localhost -w 20
   ```

## How it Works

The script first resolves the target hostname to an IP address. It then generates a list of ports to scan based on the user's input. A `ThreadPoolExecutor` is used to create a pool of worker threads. Each thread attempts to establish a TCP connection to a specific port on the target. If the connection is successful (indicated by a return code of 0 from `connect_ex`), the port is considered open. The script also tries to determine the service associated with the open port using `socket.getservbyport`.

## License

This project is open-source and available under the [MIT License](LICENSE).
