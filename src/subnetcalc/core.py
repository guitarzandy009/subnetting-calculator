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