"""Core subnetting logic — pure stdlib, no external dependencies."""


def parse_cidr(cidr: str) -> tuple[str, int]:
    """
    Parse a CIDR string like '192.168.1.0/24' into its IP and prefix length.

    Raises ValueError if the format is invalid.
    """
    if "/" not in cidr:
        raise ValueError(f"Missing '/' in CIDR notation: {cidr!r}")

    ip_part, prefix_part = cidr.split("/", 1)

    octets = ip_part.split(".")
    if len(octets) != 4:
        raise ValueError(f"IP must have 4 octets: {ip_part!r}")
    
    for octet in octets:
        if not octet.isdigit() or not (0 <= int(octet) <= 255):
            raise ValueError(f"Invalid octet: {octet!r}")

    if not prefix_part.isdigit() or not (0 <= int(prefix_part) <= 32):
        raise ValueError(f"Invalid prefix length: {prefix_part!r}")

    return ip_part, int(prefix_part)

def ip_to_int(ip: str) -> int:
    """Convert a dotted-decimal IPv4 address to a 32-bit integer."""
    octets = ip.split(".")
    return (int(octets[0]) << 24) | (int(octets[1]) << 16) | (int(octets[2]) << 8) | int(octets[3])


def int_to_ip(value: int) -> str:
    """Convert a 32-bit integer back to dotted-decimal IPv4 notation."""
    return ".".join(str((value >> shift) & 0xFF) for shift in (24, 16, 8, 0))

def prefix_to_mask_int(prefix_length: int) -> int:
    """Convert a prefix length (e.g. 24) into a 32-bit subnet mask integer."""
    if not (0 <= prefix_length <= 32):
        raise ValueError(f"Prefix length must be between 0 and 32: {prefix_length}")

    return (0xFFFFFFFF << (32 - prefix_length)) & 0xFFFFFFFF

def prefix_to_mask(prefix_length: int) -> str:
    """Convert a prefix length (e.g. 24) into a dotted-decimal subnet mask."""
    return int_to_ip(prefix_to_mask_int(prefix_length))


def network_address(ip: str, prefix_length: int) -> str:
    """Given an IP and prefix length, return the network address."""
    ip_int = ip_to_int(ip)
    mask_int = prefix_to_mask_int(prefix_length)
    network_int = ip_int & mask_int
    return int_to_ip(network_int)

def broadcast_address(ip: str, prefix_length: int) -> str:
    """Given an IP and prefix length, return the broadcast address."""
    ip_int = ip_to_int(ip)
    mask_int = prefix_to_mask_int(prefix_length)
    host_mask = ~mask_int & 0xFFFFFFFF
    broadcast_int = ip_int | host_mask
    return int_to_ip(broadcast_int)


def usable_host_range(ip: str, prefix_length: int) -> tuple[str, str]:
    """Given an IP and prefix length, return (first_usable, last_usable) as strings."""
    if prefix_length == 32:
        raise ValueError("No usable host range for /32 subnets")

    network = network_address(ip, prefix_length)
    broadcast = broadcast_address(ip, prefix_length)

    if prefix_length == 31:
        return network, broadcast

    network_int = ip_to_int(network)
    broadcast_int = ip_to_int(broadcast)

    first_usable = int_to_ip(network_int + 1)
    last_usable = int_to_ip(broadcast_int - 1)

    return first_usable, last_usable


def usable_host_count(prefix_length: int) -> int:
    """Given a prefix length, return the number of usable host addresses."""
    if not (0 <= prefix_length <= 32):
        raise ValueError(f"Prefix length must be between 0 and 32: {prefix_length}")

    if prefix_length == 32:
        return 0
    if prefix_length == 31:
        return 2

    host_bits = 32 - prefix_length
    return (2 ** host_bits) - 2

def subnet_summary(cidr: str) -> dict:
    """Given a CIDR string, return a dict with the full subnet breakdown."""
    ip, prefix_length = parse_cidr(cidr)

    summary = {
        "input": cidr,
        "ip_address": ip,
        "prefix_length": prefix_length,
        "subnet_mask": prefix_to_mask(prefix_length),
        "network_address": network_address(ip, prefix_length),
        "broadcast_address": broadcast_address(ip, prefix_length),
        "usable_host_count": usable_host_count(prefix_length),
    }

    if prefix_length < 32:
        first, last = usable_host_range(ip, prefix_length)
        summary["first_usable"] = first
        summary["last_usable"] = last
    else:
        summary["first_usable"] = None
        summary["last_usable"] = None

    return summary

