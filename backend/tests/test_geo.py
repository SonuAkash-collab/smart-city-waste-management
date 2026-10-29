"""Tests for geographic calculation helpers."""

import pytest

from app.services.geo import haversine_distance


def test_same_coordinates_return_zero():
    distance = haversine_distance(
        12.9716, 77.5946,
        12.9716, 77.5946,
    )

    assert distance == pytest.approx(0.0)


def test_known_distance_is_approximately_correct():
    distance = haversine_distance(
        12.9716, 77.5946,
        13.0827, 80.2707,
    )

    assert distance == pytest.approx(290, abs=2)


def test_distance_is_symmetric():
    distance_ab = haversine_distance(
        12.9716, 77.5946,
        13.0827, 80.2707,
    )
    distance_ba = haversine_distance(
        13.0827, 80.2707,
        12.9716, 77.5946,
    )

    assert distance_ab == pytest.approx(distance_ba)


def test_different_coordinates_return_positive_distance():
    distance = haversine_distance(
        12.9716, 77.5946,
        13.0827, 80.2707,
    )

    assert distance > 0

@pytest.mark.parametrize("latitude", [-91, 91])
def test_invalid_latitude_raises_value_error(latitude):
    with pytest.raises(ValueError, match="Latitude"):
        haversine_distance(latitude, 0, 0, 0)


@pytest.mark.parametrize("longitude", [-181, 181])
def test_invalid_longitude_raises_value_error(longitude):
    with pytest.raises(ValueError, match="Longitude"):
        haversine_distance(0, longitude, 0, 0)


@pytest.mark.parametrize("latitude", [-90, 90])
def test_latitude_boundaries_are_valid(latitude):
    distance = haversine_distance(latitude, 0, 0, 0)
    assert distance >= 0


@pytest.mark.parametrize("longitude", [-180, 180])
def test_longitude_boundaries_are_valid(longitude):
    distance = haversine_distance(0, longitude, 0, 0)
    assert distance >= 0
 