"""Tests for the shared money helper (dollars <-> cents)."""

from features.money import cents_to_dollars, dollars_to_cents


def test_dollars_to_cents_converts_whole_and_fraction():
    assert dollars_to_cents("3.99") == 399
    assert dollars_to_cents("1.25") == 125


def test_dollars_to_cents_converts_whole_dollars():
    assert dollars_to_cents("5") == 500


def test_dollars_to_cents_handles_rounding():
    assert dollars_to_cents("2.005") == 200


def test_cents_to_dollars_formats_two_decimals():
    assert cents_to_dollars(399) == "3.99"
    assert cents_to_dollars(125) == "1.25"


def test_cents_to_dollars_handles_whole_dollars():
    assert cents_to_dollars(500) == "5.00"


def test_dollars_to_cents_round_trip():
    assert cents_to_dollars(dollars_to_cents("10.99")) == "10.99"