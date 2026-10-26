"""Full-pool elevations, operators and gauge IDs for 44 US reservoirs.

The bundled table maps each named reservoir to its operating agency, its
published full-pool (conservation-pool) elevation in feet above mean sea level,
its capacity in acre-feet where published, and the identifier of the gauge that
reports its level (USGS NWIS site number or California CDEC station ID).

Levels themselves are live data and are not bundled. Use :func:`gauge_url` to
find the agency page for a reservoir, then :func:`feet_from_full` to place a
reading against the full-pool mark.
"""

import csv
import io
from collections import namedtuple
from importlib import resources

__all__ = ["Reservoir", "load", "find", "feet_from_full", "gauge_url", "by_state"]
__version__ = "0.1.0"

Reservoir = namedtuple(
    "Reservoir",
    "slug name state river operator full_pool_ft capacity_af live_data_feed usgs_site cdec_id",
)


def _num(text):
    text = (text or "").strip()
    return float(text) if text else None


def load():
    """Return every reservoir in the bundled table as a list of Reservoir tuples."""
    raw = resources.files(__package__).joinpath("reservoirs.csv").read_text(encoding="utf-8")
    rows = []
    for rec in csv.DictReader(io.StringIO(raw)):
        rows.append(
            Reservoir(
                slug=rec["slug"],
                name=rec["name"],
                state=rec["state"],
                river=rec["river"],
                operator=rec["operator"],
                full_pool_ft=_num(rec["full_pool_ft"]),
                capacity_af=_num(rec["capacity_af"]),
                live_data_feed=rec["live_data_feed"] or None,
                usgs_site=rec["usgs_site"] or None,
                cdec_id=rec["cdec_id"] or None,
            )
        )
    return rows


def _norm(text):
    return "".join(ch for ch in text.lower() if ch.isalnum())


def find(query):
    """Find one reservoir by slug, exact name, or a unique case-insensitive name fragment.

    Raises KeyError if nothing matches and ValueError if the fragment is ambiguous.
    """
    q = _norm(query)
    rows = load()
    for r in rows:
        if q in (_norm(r.slug), _norm(r.name)):
            return r
    hits = [r for r in rows if q and q in _norm(r.name)]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise KeyError(query)
    raise ValueError("ambiguous: %s matches %s" % (query, ", ".join(h.name for h in hits)))


def by_state(state):
    """All reservoirs in a two-letter state, in table order."""
    s = state.strip().upper()
    return [r for r in load() if r.state == s]


def feet_from_full(reservoir, elevation_ft):
    """Elevation minus full pool, in feet. Negative means below full.

    ``reservoir`` may be a Reservoir or anything :func:`find` accepts.
    """
    r = reservoir if isinstance(reservoir, Reservoir) else find(reservoir)
    if r.full_pool_ft is None:
        raise ValueError("no published full-pool elevation for %s" % r.name)
    return round(float(elevation_ft) - r.full_pool_ft, 2)


def gauge_url(reservoir):
    """Agency web page for the reservoir's gauge, or None when the table carries no ID."""
    r = reservoir if isinstance(reservoir, Reservoir) else find(reservoir)
    if r.usgs_site:
        return "https://waterdata.usgs.gov/monitoring-location/%s/" % r.usgs_site
    if r.cdec_id:
        return "https://cdec.water.ca.gov/dynamicapp/staMeta?station_id=%s" % r.cdec_id
    return None
