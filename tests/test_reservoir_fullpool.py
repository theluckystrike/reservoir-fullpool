import pytest

import reservoir_fullpool as rf


def test_table_size_and_fields():
    rows = rf.load()
    assert len(rows) == 44
    assert len({r.slug for r in rows}) == 44
    assert all(r.full_pool_ft is not None for r in rows)


def test_find_variants():
    assert rf.find("lake-travis").full_pool_ft == 681
    assert rf.find("Lake Travis").operator.startswith("LCRA")
    assert rf.find("buchanan").usgs_site == "08148000"
    with pytest.raises(KeyError):
        rf.find("no such lake")
    with pytest.raises(ValueError):
        rf.find("lake")


def test_feet_from_full():
    assert rf.feet_from_full("Lake Travis", 677.23) == -3.77
    assert rf.feet_from_full("Lake Mead", 1229) == 0.0


def test_gauge_urls():
    assert rf.gauge_url("Lake Powell") == "https://waterdata.usgs.gov/monitoring-location/09379900/"
    assert rf.gauge_url("Shasta Lake").endswith("station_id=SHA")
    assert rf.gauge_url("Lake Travis") is None


def test_by_state():
    assert {r.state for r in rf.by_state("ca")} == {"CA"}
    assert len(rf.by_state("TX")) >= 10
