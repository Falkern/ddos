# DDoS Attack Scripts

This repository contains Python scripts designed to simulate different types of Distributed Denial of Service (DDoS) attacks. These scripts are intended for educational purposes only. Unauthorized use of these scripts to attack networks is illegal and unethical. Always obtain proper authorization before testing network security.

## Prerequisites

- Python 3.x
- Required libraries: `requests`, `httpx`, `scapy`

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Falkern/ddos-attack.git
   ```
2. Navigate to the project directory:
   ```sh
   cd ddos-attack
   ```
3. Install the required libraries

## Scripts

### `ddos_any_site.py`

This script performs a HTTP-based stress test on a specified URL. It sends multiple HTTP GET requests to the target URL using either synchronous or asynchronous methods. The script includes features such as retries, exponential backoff, and rate limiting.

#### Usage

Run the script with the following command:

```sh
python ddos_any_site.py
```

You will be prompted to enter the target URL, number of requests, maximum number of threads, minimum delay, and maximum delay between requests. You can also choose to use asynchronous mode for high volume requests.

### `ddos_attack.py`

This script simulates a DHCP-based DDoS attack. It generates DHCP discovery packets with random MAC addresses to flood a network. The script uses the Scapy library to craft and send the packets.

#### Usage

Run the script with the following command:

```sh
python ddos_attack.py
```

## Disclaimer

These scripts are intended for educational purposes only. Unauthorized use of these scripts to attack networks is illegal and unethical. Always obtain proper authorization before testing network security.
