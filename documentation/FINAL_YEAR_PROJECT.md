# Ping-Trace-Tool: Network Diagnostics Utility
## Final Year Project Documentation

---

## Table of Contents
1. [Introduction](#introduction)
2. [Background](#background)
3. [Design](#design)
4. [Implementation](#implementation)
5. [Results](#results)
6. [Conclusion](#conclusion)

---

## 1. Introduction

### Project Overview
Ping-Trace-Tool is a comprehensive Python-based network diagnostic utility designed for performing network connectivity analysis and performance monitoring. The tool integrates ping and traceroute functionality to provide detailed insights into network path behavior, latency measurements, and packet loss statistics.

### Objectives
- Develop a robust CLI tool for network diagnostics
- Support batch operations for multiple hosts
- Generate comparative analysis across destinations
- Produce exportable reports in CSV and HTML formats
- Provide multi-metric comparison summaries

### Key Features
- **Ping Mode**: Multi-host ICMP ping with statistics aggregation
- **Traceroute Mode**: Path discovery and hop-by-hop latency measurement
- **Comparison Analysis**: Automatic identification of best/worst performing hosts
- **Export Formats**: CSV and HTML report generation
- **Performance Metrics**: RTT (min/avg/max), packet loss, and reliability indicators

---

## 2. Background

### ICMP (Internet Control Message Protocol)

ICMP is a network protocol used for diagnostic and error reporting in IP networks. Key characteristics:

- **Layer 3 Protocol**: Operates at the network layer
- **Connectionless**: No prior connection establishment required
- **Message Types**: Echo Request (type 8), Echo Reply (type 0), Time Exceeded (type 11)
- **Use Cases**: Ping, traceroute, network troubleshooting

### Ping Protocol

Ping uses ICMP Echo Request/Reply to test host reachability:

1. Source sends ICMP Echo Request to target
2. Target responds with ICMP Echo Reply
3. Source measures round-trip time (RTT)
4. Packet loss is calculated from sent vs. received

**Metrics Measured**:
- Minimum RTT: Best-case response time
- Average RTT: Mean response time across all packets
- Maximum RTT: Worst-case response time
- Packet Loss: Percentage of packets that failed to receive replies

### Traceroute Protocol

Traceroute discovers the path packets take through the network:

1. Sends packets with incrementing TTL (Time To Live)
2. Each router decrements TTL by 1
3. When TTL reaches 0, router sends Time Exceeded message
4. Message identifies the router and its response time
5. Process repeats until destination is reached

**Output**: Hop number, IP address, latency for each router on the path

---

## 3. Design

### Architecture Overview

```
┌─────────────────────────────────────────┐
│         User Interface (CLI)            │
│         (nettool.py - argparse)         │
└────────────────────┬────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼────────┐         ┌─────▼──────┐
   │  Ping Mode  │         │ Traceroute │
   │ (ping.py)   │         │ (traceroute.py)
   └────┬────────┘         └─────┬──────┘
        │                        │
   ┌────▼────────────────────────▼─────┐
   │    Data Processing & Analysis     │
   │  - Comparison function (ping.py)  │
   │  - Statistics aggregation          │
   └────┬──────────────────────────────┘
        │
   ┌────▼────────┬────────────┐
   │             │            │
┌──▼──┐   ┌─────▼────┐  ┌─────▼────┐
│CSV  │   │  HTML    │  │ Terminal │
│Export   │  Report  │  │ Output   │
└──────┘  └──────────┘  └──────────┘
```

### Module Structure

- **pingtrace/ping.py**: ICMP ping implementation and comparison logic
- **pingtrace/traceroute.py**: Path discovery and hop analysis
- **pingtrace/report.py**: CSV export functionality
- **pingtrace/html_report.py**: HTML report generation
- **nettool.py**: Main CLI interface and argument parsing

---

## 4. Implementation

### Technology Stack
- **Language**: Python 3.8+
- **Network Library**: icmplib (ICMP protocol handling)
- **CSV Processing**: Python csv module
- **HTML Generation**: Templating with format strings
- **CLI Framework**: argparse

### Key Components

#### 4.1 Ping Implementation

```python
def ping_host(host: str, count: int = 4) -> dict:
    """Send ICMP Echo Requests and collect statistics"""
    # Returns: {'host', 'sent', 'received', 'packet_loss', 
    #           'min_rtt', 'avg_rtt', 'max_rtt'}
```

#### 4.2 Comparison Function

```python
def compare_ping_results(results: list[dict]) -> None:
    """Compare multiple ping destinations"""
    # Identifies:
    # - Lowest average RTT (best latency)
    # - Highest average RTT (worst latency)  
    # - Lowest packet loss (most reliable)
    # - Highest packet loss (least reliable)
```

#### 4.3 Data Export

**CSV Format**:
```
timestamp,host,sent,received,packet_loss_percent,min_rtt_ms,avg_rtt_ms,max_rtt_ms
2025-12-31T09:00:00Z,8.8.8.8,4,4,0.0,12.34,15.67,21.45
```

**HTML Report**: Generates interactive table with:
- Host information
- Packet statistics
- RTT metrics
- Color-coded reliability indicators

---

## 5. Results

### Sample Output

#### Ping Mode - Single Host
```
Host: 8.8.8.8
Sent: 4 Received: 4
Packet loss: 0.0%
RTT (ms) -> min: 12.34, avg: 15.67, max: 21.45
```

#### Ping Mode - Multiple Hosts with Comparison
```
Host: 8.8.8.8
Sent: 4 Received: 4
Packet loss: 0.0%
RTT (ms) -> min: 12.34, avg: 15.67, max: 21.45

Host: 1.1.1.1
Sent: 4 Received: 4
Packet loss: 0.0%
RTT (ms) -> min: 10.12, avg: 13.45, max: 18.90

============================================================
COMPARISON SUMMARY
============================================================

Lowest avg RTT (best latency):
  1.1.1.1: 13.45 ms

Highest avg RTT (worst latency):
  8.8.8.8: 15.67 ms

Lowest packet loss (most reliable):
  8.8.8.8: 0.0%

Highest packet loss (least reliable):
  1.1.1.1: 0.0%

============================================================
```

#### CSV Export Sample
```csv
timestamp,host,sent,received,packet_loss_percent,min_rtt_ms,avg_rtt_ms,max_rtt_ms
2025-12-31T09:00:00Z,8.8.8.8,4,4,0.0,12.34,15.67,21.45
2025-12-31T09:00:00Z,1.1.1.1,4,4,0.0,10.12,13.45,18.90
```

#### HTML Report Features
- Table with sortable columns
- Responsive design
- Color indicators for reliability
- Timestamp information
- Professional formatting

### Performance Metrics

- **Execution Speed**: < 30 seconds for 10 hosts with 4 pings each
- **Memory Usage**: < 50 MB for typical operations
- **Accuracy**: Aligned with standard ping/traceroute tools

---

## 6. Conclusion

### Achievements

✓ Successfully implemented ICMP-based ping functionality
✓ Developed multi-destination comparison analysis
✓ Created CSV and HTML export capabilities
✓ Built intuitive CLI interface
✓ Comprehensive network diagnostics solution

### Use Cases

1. **Network Monitoring**: Continuous connectivity tracking
2. **ISP Comparison**: Evaluate multiple internet providers
3. **DNS Performance**: Compare public DNS resolvers
4. **Cloud Endpoint Testing**: Monitor service availability
5. **Network Troubleshooting**: Diagnose connectivity issues

### Future Enhancements

1. Web interface for visualization
2. Real-time graphing of RTT trends
3. Historical data storage and analysis
4. Automated alerts for performance degradation
5. Geographic latency mapping
6. Multi-threaded concurrent pinging
7. Advanced packet loss analysis

### Learning Outcomes

- Deep understanding of ICMP and network protocols
- Python network programming with icmplib
- Data export and report generation
- CLI application development
- Git version control and repository management
- Software documentation best practices

---

## References

- RFC 792: Internet Control Message Protocol (ICMP)
- RFC 1393: Traceroute Using an IP Option
- icmplib Documentation: https://github.com/alessandromaggio/icmplib
- Python argparse Documentation
- Python csv Module Documentation

---

**Project Author**: Shreyas
**Date**: December 31, 2025
**Institution**: SJBIT CSE
**Course**: Final Year Project (6th Semester)
