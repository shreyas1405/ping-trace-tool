## CSV export for ping results

The tool can export aggregated ping statistics to a CSV file for further analysis or integration with other systems. The CSV export is handled by the `write_ping_csv` helper in `pingtrace/report.py`.

### Output format

Each row in the CSV represents ping statistics for a single host at a given time. The file includes the following columns:

- `timestamp`: UTC timestamp in ISO 8601 format when the report was generated  
- `host`: Target host or IP address  
- `sent`: Number of ICMP echo requests sent  
- `received`: Number of ICMP echo replies received  
- `packet_loss_percent`: Packet loss expressed as a percentage  
- `min_rtt_ms`: Minimum round-trip time in milliseconds  
- `avg_rtt_ms`: Average round-trip time in milliseconds  
- `max_rtt_ms`: Maximum round-trip time in milliseconds

### Programmatic usage

You can call the CSV export directly from Python code by passing a filename and a list of result dictionaries.

```python
from pingtrace.report import write_ping_csv

results = [
    {
        "host": "8.8.8.8",
        "sent": 4,
        "received": 4,
        "packet_loss": 0.0,        # fraction between 0 and 1
        "min_rtt": 12.3,
        "avg_rtt": 15.7,
        "max_rtt": 21.4,
    },
]

write_ping_csv("ping_report.csv", results)
```

Each result dictionary must contain the keys `host`, `sent`, `received`, `packet_loss`, `min_rtt`, `avg_rtt`, and `max_rtt`, which are then transformed into the structured CSV format described above.
