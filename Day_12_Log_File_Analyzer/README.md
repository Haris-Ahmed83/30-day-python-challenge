# Day 12: Log File Analyzer

A professional Python-based log file analyzer designed to parse server logs, produce statistical reports, and detect anomalies such as high traffic volumes or excessive HTTP errors.

## Features

- **Regex-based Parsing**: Efficiently parses Apache/Nginx Common Log Format.
- **Statistical Summaries**:
  - Total requests and bandwidth usage.
  - Distribution of HTTP status codes.
  - Identification of top-performing IP addresses and requested paths.
- **Anomaly Detection**:
  - Automatically detects and reports 4xx and 5xx HTTP errors.
  - Identifies potential high-traffic anomalies based on a request threshold.
- **CLI Interface**: Command-line arguments for file input and sample generation.

## Usage

### Run with a sample log file
```bash
python log_analyzer.py --generate-sample
```

### Analyze an existing log file
```bash
python log_analyzer.py --file your_access.log
```

## Requirements
- Python 3.x
- Standard library modules (`re`, `json`, `argparse`, `collections`, `datetime`)
