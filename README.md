# Hostname Processing and Verification Script Documentation

This script is designed to process a hostname file, check the status of IPs associated with those hostnames, perform reverse lookup, verify if IPs belong to the correct subnet, and export the results to a CSV file.

It uses **asyncio** for asynchronous and efficient processing of multiple hostnames, **socket** for IP resolution and reverse lookup, and **aiohttp** for non-blocking network operations.

## Features

1. **Hostname to IP Resolution**:
   - The `get_ip_from_hostname()` function resolves the IP address of a given hostname.

2. **IP Status Check**:
   - The `check_status()` function uses the `ping` command to check whether an IP is "Online" or "Offline".

3. **IP Reverse Lookup**:
   - The script performs a reverse lookup using the `reverse_lookup()` function to verify if the IP resolves to a matching hostname.

4. **Subnet Verification**:
   - If the hostname and resolved IP do not match as expected, the script scans the subnet to find other associated IPs and validates them.

5. **CSV Export**:
   - The script exports the results for each hostname and its associated IP to a CSV file using the `export_results_to_csv()` function.

6. **Results Display**:
   - Results are displayed in a tabulated format using the `tabulate` library, showing hostname, resolved IP, status, and subnet verification.

7. **Dynamic Concurrency**:
   - Concurrency is dynamically adjusted to ensure efficient use of system resources, limiting the number of simultaneous tasks based on system load.

## Code Structure

### 1. Asynchronous Functions

- **`get_ip_from_hostname()`**: Resolves hostname to IP.
- **`reverse_lookup()`**: Performs a reverse lookup of an IP.
- **`check_status()`**: Checks if an IP is online.
- **`scan_subnet()`**: Scans other IPs in the subnet.
- **`check_ip()`**: Verifies each IP, including subnet validation.

### 2. Export Function

- **`export_results_to_csv()`**: Exports the collected results to a CSV file.

### 3. Main Function `process_hostnames()`

```python
async def process_hostnames(input_file_path, export_file_name):
```

- Processes a list of hostnames from a text file.
- Resolves the IP of each hostname and performs reverse lookup.
- Scans the subnet if the resolved IP does not match expectations.
- Displays and exports results to a CSV file.

### 4. Individual Hostname Processing Function

```python
async def process_hostname(hostname, results, semaphore):
```

- Resolves each hostname and checks IP status.
- If the reverse lookup does not match, scans the subnet.

### 5. Asynchronous Execution

```python
asyncio.run(process_hostnames(input_file_path, export_file_name))
```

Starts script execution, requesting the hostname file path and export file name for the results.

## Function Details

### `get_ip_from_hostname()`

Resolves the IP address of a given hostname. Returns `None` if resolution fails.

### `reverse_lookup()`

Performs a reverse lookup to find the name associated with the IP.

### `check_status()`

Checks IP status using the `ping` command. Returns "Online" if reachable, otherwise "Offline".

### `scan_subnet()`

Scans all IPs within a subnet (excluding the already verified IP) and validates them to match the given hostname.

### `get_dynamic_semaphore()`

Dynamically determines the number of concurrent tasks based on CPU cores to avoid overloading the system.

### `export_results_to_csv()`

Exports results to a CSV file with columns: `Hostname`, `Resolved IP`, `Status`, `Checked in Subnet`.

### `process_hostnames()`

Processes the hostname file, resolves IPs, checks status, and exports results to CSV. Also displays data in a tabulated format on screen.

## Input Example

The script expects a text file with one hostname per line. Example content of `hostnames.txt`:

```
example.com
testhost.local
server1.mydomain.com
```

## Example Output in CSV

The generated `resultado_hostnames.csv` will have the following format:

| Hostname            | Resolved IP     | Status  | Checked in Subnet |
|---------------------|------------------|---------|--------------------|
| example.com         | 93.184.216.34    | Online  | No                 |
| testhost.local      | 192.168.1.100    | Offline | No                 |
| server1.mydomain.com| 10.0.0.1         | Online  | Yes                |

## Possible Improvements

- **Resolution Error Handling**: Improve IP resolution error management to ensure unresolved hostnames are properly logged.
- **Ping Timeout**: Adjust ping timeout as needed, depending on network latency.
- **IPv6 Support**: Add IPv6 support if required by the network environment.

## Conclusion

This script is an efficient tool for managing and verifying hostnames in a network, with features for IP resolution, reverse lookup, and status checking. It also facilitates CSV export of results, which is useful for analysis and reporting.
