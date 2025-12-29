import argparse
from pingtrace.ping import ping_host


def main():
    parser = argparse.ArgumentParser(description="Ping (and later traceroute) tool.")
    parser.add_argument("hosts", nargs="+", help="Hostnames or IP addresses to ping")
    parser.add_argument("--count", type=int, default=4, help="Number of echo requests per host")
    args = parser.parse_args()

    for host in args.hosts:
        stats = ping_host(host, count=args.count)
        print(f"\nHost: {stats['host']}")
        print(f"Sent: {stats['sent']}  Received: {stats['received']}")
        print(f"Packet loss: {stats['packet_loss'] * 100:.1f}%")
        print(
            f"RTT (ms) -> min: {stats['min_rtt']:.2f}, "
            f"avg: {stats['avg_rtt']:.2f}, max: {stats['max_rtt']:.2f}"
        )


if __name__ == "__main__":
    main()
