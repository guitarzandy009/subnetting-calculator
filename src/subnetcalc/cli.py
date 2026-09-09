import argparse

from subnetcalc.core import subnet_summary


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argparse parser for the subnetcalc CLI."""
    parser = argparse.ArgumentParser(
        prog="subnetcalc",
        description="Calculate subnet details from an IPv4 address in CIDR notation.",
    )
    parser.add_argument(
        "cidr",
        help="IP address in CIDR notation, e.g. 192.168.1.0/24",
    )
    return parser


def main() -> None:
    """Parse command-line arguments, compute the subnet summary, and print it."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        summary = subnet_summary(args.cidr)
    except ValueError as e:
        parser.error(str(e))
        return

    print(f"Input:              {summary['input']}")
    print(f"IP address:         {summary['ip_address']}")
    print(f"Prefix length:      /{summary['prefix_length']}")
    print(f"Subnet mask:        {summary['subnet_mask']}")
    print(f"Network address:    {summary['network_address']}")
    print(f"Broadcast address:  {summary['broadcast_address']}")
    if summary["first_usable"] is not None:
        print(f"Usable host range:  {summary['first_usable']} - {summary['last_usable']}")
    else:
        print("Usable host range:  N/A (no usable hosts at this prefix)")
    print(f"Usable host count:  {summary['usable_host_count']}")


if __name__ == "__main__":
    main()