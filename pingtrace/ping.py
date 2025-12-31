from icmplib import ping


def ping_host(host: str, count: int = 4, interval: float = 0.5, timeout: float = 2.0) -> dict:
    """
    Ping a host and return statistics.
    """
    result = ping(
        host,
        count=count,
        interval=interval,
        timeout=timeout,
        privileged=False  # non-root mode on Linux. [web:40][web:74]
    )

    return {
        "host": host,
        "sent": result.packets_sent,
        "received": result.packets_received,
        "packet_loss": result.packet_loss,      # 0.0–1.0 fraction. [web:23]
        "min_rtt": result.min_rtt,              # ms
        "avg_rtt": result.avg_rtt,
        "max_rtt": result.max_rtt,
    }


def compare_ping_results(results: list[dict]) -> None:
    """
    Compare ping results across multiple hosts and print a summary.
    Identifies: lowest avg RTT, highest packet loss, best/worst performance.
    """
    if not results:
        return
    
    if len(results) == 1:
        return  # No comparison needed for single host
    
    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    
    # Lowest average RTT (best latency)
    best_rtt_host = min(results, key=lambda x: x["avg_rtt"])
    print(f"\nLowest avg RTT (best latency):")
    print(f"  {best_rtt_host['host']}: {best_rtt_host['avg_rtt']:.2f} ms")
    
    # Highest average RTT (worst latency)
    worst_rtt_host = max(results, key=lambda x: x["avg_rtt"])
    print(f"\nHighest avg RTT (worst latency):")
    print(f"  {worst_rtt_host['host']}: {worst_rtt_host['avg_rtt']:.2f} ms")
    
    # Lowest packet loss (most reliable)
    best_loss_host = min(results, key=lambda x: x["packet_loss"])
    print(f"\nLowest packet loss (most reliable):")
    print(f"  {best_loss_host['host']}: {best_loss_host['packet_loss']*100:.1f}%")
    
    # Highest packet loss (least reliable)
    worst_loss_host = max(results, key=lambda x: x["packet_loss"])
    print(f"\nHighest packet loss (least reliable):")
    print(f"  {worst_loss_host['host']}: {worst_loss_host['packet_loss']*100:.1f}%")
    
    print("\n" + "="*60)
