import pytest

from subnetcalc.core import parse_cidr


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