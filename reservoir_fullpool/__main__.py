"""python -m reservoir_fullpool NAME [ELEVATION_FT]"""

import sys

from . import feet_from_full, find, gauge_url


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print("usage: python -m reservoir_fullpool NAME [ELEVATION_FT]")
        return 2
    r = find(args[0])
    print("%s (%s), %s" % (r.name, r.state, r.operator))
    if r.full_pool_ft is not None:
        print("full pool: %g ft msl" % r.full_pool_ft)
    if r.capacity_af is not None:
        print("capacity: %s acre-feet" % format(int(r.capacity_af), ","))
    url = gauge_url(r)
    if url:
        print("gauge: %s" % url)
    if len(args) > 1:
        d = feet_from_full(r, float(args[1]))
        side = "above" if d > 0 else "below" if d < 0 else "at"
        print("%s ft is %s full pool by %.2f ft" % (args[1], side, abs(d)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
