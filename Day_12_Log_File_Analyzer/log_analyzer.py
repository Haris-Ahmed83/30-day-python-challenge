import re
import json
import argparse
from collections import Counter
from datetime import datetime

class LogAnalyzer:
    """
    A professional log file analyzer to parse, analyze, and detect anomalies in server logs.
    """
    def __init__(self, log_format=None):
        # Default Apache/Nginx Common Log Format
        self.log_pattern = re.compile(
            r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>.*?)\] "(?P<method>\w+) (?P<path>.*?) HTTP/.*?" (?P<status>\d+) (?P<size>\d+)'
        )
        self.results = {
            "total_requests": 0,
            "status_codes": Counter(),
            "ip_addresses": Counter(),
            "top_paths": Counter(),
            "total_bandwidth": 0,
            "anomalies": []
        }

    def parse_line(self, line):
        match = self.log_pattern.match(line)
        if match:
            data = match.groupdict()
            data['status'] = int(data['status'])
            data['size'] = int(data['size'])
            return data
        return None

    def analyze(self, file_path):
        with open(file_path, 'r') as f:
            for line in f:
                data = self.parse_line(line.strip())
                if not data:
                    continue

                self.results["total_requests"] += 1
                self.results["status_codes"][data['status']] += 1
                self.results["ip_addresses"][data['ip']] += 1
                self.results["top_paths"][data['path']] += 1
                self.results["total_bandwidth"] += data['size']

                # Simple Anomaly Detection: 4xx/5xx errors or high request volume from one IP
                if data['status'] >= 400:
                    self.results["anomalies"].append({
                        "type": "HTTP Error",
                        "ip": data['ip'],
                        "status": data['status'],
                        "path": data['path'],
                        "timestamp": data['timestamp']
                    })

        self.detect_volume_anomalies()

    def detect_volume_anomalies(self, threshold=100):
        for ip, count in self.results["ip_addresses"].items():
            if count > threshold:
                self.results["anomalies"].append({
                    "type": "High Traffic",
                    "ip": ip,
                    "count": count,
                    "description": f"IP {ip} made {count} requests (Threshold: {threshold})"
                })

    def generate_report(self):
        report = []
        report.append("="*40)
        report.append(" SERVER LOG ANALYSIS REPORT ")
        report.append("="*40)
        report.append(f"Total Requests: {self.results['total_requests']}")
        report.append(f"Total Bandwidth: {self.results['total_bandwidth'] / (1024*1024):.2f} MB")
        
        report.append("\n[Status Codes]")
        for code, count in self.results["status_codes"].most_common():
            report.append(f"  {code}: {count}")

        report.append("\n[Top 5 IP Addresses]")
        for ip, count in self.results["ip_addresses"].most_common(5):
            report.append(f"  {ip}: {count}")

        report.append("\n[Top 5 Requested Paths]")
        for path, count in self.results["top_paths"].most_common(5):
            report.append(f"  {path}: {count}")

        report.append("\n[Anomalies Detected]")
        if not self.results["anomalies"]:
            report.append("  No significant anomalies detected.")
        else:
            for anomaly in self.results["anomalies"][:10]: # Show first 10
                if anomaly['type'] == "HTTP Error":
                    report.append(f"  - {anomaly['type']}: {anomaly['status']} on {anomaly['path']} by {anomaly['ip']}")
                else:
                    report.append(f"  - {anomaly['type']}: {anomaly['description']}")

        return "\n".join(report)

def generate_sample_log(file_path):
    """Generates a sample log file for demonstration."""
    samples = [
        '192.168.1.1 - - [06/Mar/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024',
        '192.168.1.2 - - [06/Mar/2026:10:00:02 +0000] "GET /about.html HTTP/1.1" 200 2048',
        '192.168.1.1 - - [06/Mar/2026:10:00:03 +0000] "POST /login HTTP/1.1" 401 512',
        '10.0.0.5 - - [06/Mar/2026:10:00:04 +0000] "GET /admin HTTP/1.1" 403 128',
        '192.168.1.3 - - [06/Mar/2026:10:00:05 +0000] "GET /api/data HTTP/1.1" 500 256',
    ]
    with open(file_path, 'w') as f:
        for _ in range(20): # Add some normal traffic
            for line in samples:
                f.write(line + "\n")
        # Add a volume anomaly
        for _ in range(150):
            f.write('1.2.3.4 - - [06/Mar/2026:11:00:00 +0000] "GET /attack HTTP/1.1" 200 64\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Professional Log File Analyzer")
    parser.add_argument("--file", help="Path to the log file to analyze")
    parser.add_argument("--generate-sample", action="store_true", help="Generate a sample log file for testing")
    args = parser.parse_args()

    analyzer = LogAnalyzer()
    
    log_file = args.file
    if args.generate_sample:
        log_file = "sample_access.log"
        generate_sample_log(log_file)
        print(f"Sample log generated: {log_file}")

    if log_file:
        try:
            analyzer.analyze(log_file)
            print(analyzer.generate_report())
        except FileNotFoundError:
            print(f"Error: File {log_file} not found.")
    else:
        parser.print_help()
