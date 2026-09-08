import pytest

from subnetcalc.core import parse_cidr, ip_to_int, int_to_ip, prefix_to_mask_int, prefix_to_mask, network_address, broadcast_address, usable_host_range, usable_host_count, subnet_summary


def test_parse_cidr_valid():
    assert parse_cidr("192.168.1.0/24") == ("192.168.1.0", 24)


def test_parse_cidr_valid_edge_prefixes():
    assert parse_cidr("10.0.0.0/0") == ("10.0.0.0", 0)
    assert parse_cidr("10.0.0.1/32") == ("10.0.0.1", 32)


def test_parse_cidr_missing_slash():
    with pytest.raises(ValueError, match="Missing '/'"):
        parse_cidr("192.168.1.0")


def test_parse_cidr_bad_octet_count():
    with pytest.raises(ValueError, match="4 octets"):
        parse_cidr("192.168.1/24")


def test_parse_cidr_octet_out_of_range():
    with pytest.raises(ValueError, match="Invalid octet"):
        parse_cidr("192.168.1.999/24")


def test_parse_cidr_prefix_out_of_range():
    with pytest.raises(ValueError, match="Invalid prefix"):
        parse_cidr("192.168.1.0/33")

def test_ip_to_int_basic():
    assert ip_to_int("192.168.1.1") == 3232235777


def test_ip_to_int_zero():
    assert ip_to_int("0.0.0.0") == 0


def test_ip_to_int_max():
    assert ip_to_int("255.255.255.255") == 4294967295


def test_int_to_ip_basic():
    assert int_to_ip(3232235777) == "192.168.1.1"


def test_int_to_ip_zero():
    assert int_to_ip(0) == "0.0.0.0"


def test_int_to_ip_max():
    assert int_to_ip(4294967295) == "255.255.255.255"


def test_ip_to_int_and_back_round_trip():
    original = "10.20.30.40"
    assert int_to_ip(ip_to_int(original)) == original

def test_prefix_to_mask_int_24():
    assert prefix_to_mask_int(24) == 0xFFFFFF00


def test_prefix_to_mask_int_zero():
    assert prefix_to_mask_int(0) == 0


def test_prefix_to_mask_int_max():
    assert prefix_to_mask_int(32) == 0xFFFFFFFF


def test_prefix_to_mask_invalid_negative():
    with pytest.raises(ValueError, match="between 0 and 32"):
        prefix_to_mask_int(-1)


def test_prefix_to_mask_invalid_too_large():
    with pytest.raises(ValueError, match="between 0 and 32"):
        prefix_to_mask_int(33)


def test_prefix_to_mask_24():
    assert prefix_to_mask(24) == "255.255.255.0"


def test_prefix_to_mask_16():
    assert prefix_to_mask(16) == "255.255.0.0"


def test_prefix_to_mask_30():
    assert prefix_to_mask(30) == "255.255.255.252"


def test_prefix_to_mask_zero():
    assert prefix_to_mask(0) == "0.0.0.0"


def test_prefix_to_mask_max():
    assert prefix_to_mask(32) == "255.255.255.255"


def test_network_address_slash_24():
    assert network_address("192.168.1.122", 24) == "192.168.1.0"


def test_network_address_slash_16():
    assert network_address("10.5.130.7", 16) == "10.5.0.0"


def test_network_address_slash_26():
    assert network_address("172.16.5.200", 26) == "172.16.5.192"


def test_network_address_already_network():
    assert network_address("192.168.1.0", 24) == "192.168.1.0"


def test_network_address_slash_32():
    assert network_address("192.168.1.55", 32) == "192.168.1.55"


def test_network_address_slash_0():
    assert network_address("192.168.1.55", 0) == "0.0.0.0"


def test_broadcast_address_slash_24():
    assert broadcast_address("192.168.1.122", 24) == "192.168.1.255"


def test_broadcast_address_slash_16():
    assert broadcast_address("10.5.130.7", 16) == "10.5.255.255"


def test_broadcast_address_slash_26():
    assert broadcast_address("172.16.5.200", 26) == "172.16.5.255"


def test_broadcast_address_slash_32():
    assert broadcast_address("192.168.1.55", 32) == "192.168.1.55"


def test_broadcast_address_slash_0():
    assert broadcast_address("192.168.1.55", 0) == "255.255.255.255"


def test_usable_host_range_slash_24():
    assert usable_host_range("192.168.1.5", 24) == ("192.168.1.1", "192.168.1.254")


def test_usable_host_range_slash_26():
    assert usable_host_range("172.16.5.200", 26) == ("172.16.5.193", "172.16.5.254")


def test_usable_host_range_slash_30():
    assert usable_host_range("10.0.0.9", 30) == ("10.0.0.9", "10.0.0.10")


def test_usable_host_range_slash_31_raises():
    with pytest.raises(ValueError, match="No usable host range"):
        usable_host_range("192.168.1.5", 31)


def test_usable_host_range_slash_32_raises():
    with pytest.raises(ValueError, match="No usable host range"):
        usable_host_range("192.168.1.5", 32)


def test_usable_host_count_slash_24():
    assert usable_host_count(24) == 254


def test_usable_host_count_slash_26():
    assert usable_host_count(26) == 62


def test_usable_host_count_slash_30():
    assert usable_host_count(30) == 2


def test_usable_host_count_slash_31():
    assert usable_host_count(31) == 2


def test_usable_host_count_slash_32():
    assert usable_host_count(32) == 0


def test_usable_host_count_slash_0():
    assert usable_host_count(0) == 4294967294


def test_usable_host_count_invalid_negative():
    with pytest.raises(ValueError, match="between 0 and 32"):
        usable_host_count(-1)


def test_usable_host_count_invalid_too_large():
    with pytest.raises(ValueError, match="between 0 and 32"):
        usable_host_count(33)

def test_subnet_summary_slash_24():
    summary = subnet_summary("192.168.1.0/24")
    assert summary["network_address"] == "192.168.1.0"
    assert summary["broadcast_address"] == "192.168.1.255"
    assert summary["subnet_mask"] == "255.255.255.0"
    assert summary["first_usable"] == "192.168.1.1"
    assert summary["last_usable"] == "192.168.1.254"
    assert summary["usable_host_count"] == 254


def test_subnet_summary_slash_32_no_usable_range():
    summary = subnet_summary("192.168.1.5/32")
    assert summary["first_usable"] is None
    assert summary["last_usable"] is None
    assert summary["usable_host_count"] == 0


def test_subnet_summary_invalid_cidr_raises():
    with pytest.raises(ValueError):
        subnet_summary("garbage")