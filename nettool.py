import argparse
from pingtrace.ping import ping_host
from pingtrace.traceroute import traceroute_host


def run_ping(hosts, count: int):
    for host in hosts:
        stats = ping_host(host, count=count)
        print(f"\nHost: {stats['host']}")
        print(f"Sent: {stats['sent']}  Received: {stats['received']}")
        print(f"Packet loss: {stats['packet_loss'] * 100:.1f}%")
        print(
            f"RTT (ms) -> min: {stats['min_rtt']:.2f}, "
            f"avg: {stats['avg_rtt']:.2f}, max: {stats['max_rtt']:.2f}"
        )


def run_traceroute(host: str, max_hops: int):
    print(f"Traceroute to {host} (max hops: {max_hops})")
    hops = traceroute_host(host, max_hops=max_hops)
    print(f"{'Hop':<5}{'IP Address':<20}{'RTT (ms)':<10}")
    print("-" * 40)
    for hop in hops:
        ip = hop["ip"] if hop["ip"] is not None else "*"
        rtt = f"{hop['rtt_ms']:.3f}" if hop["rtt_ms"] is not None else "*"
        print(f"{hop['hop']:<5}{ip:<20}{rtt:<10}")


def main():
    parser = argparse.ArgumentParser(description="Ping and traceroute tool.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ping", action="store_true", help="Run ping mode")
    group.add_argument("--trace", action="store_true", help="Run traceroute mode")

    parser.add_argument("hosts", nargs="+", help="Hostnames or IPs")
    parser.add_argument("--count", type=int, default=4, help="Echo requests per host (ping mode)")
    parser.add_argument("--max-hops", type=int, default=30, help="Max hops (traceroute mode)")

    args = parser.parse_args()

    if args.ping:
        run_ping(args.hosts, count=args.count)
    elif args.trace:
        if len(args.hosts) != 1:
            raise SystemExit("Traceroute mode expects exactly one host.")
        run_traceroute(args.hosts[0], max_hops=args.max_hops)


if __name__ == "__main__":
    main()

