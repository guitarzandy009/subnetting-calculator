import pytest

from subnetcalc.core import parse_cidr, ip_to_int, int_to_ip, prefix_to_mask_int, prefix_to_mask, network_address, broadcast_address


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