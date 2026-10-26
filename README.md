# reservoir-fullpool

Full-pool elevations, operating agencies and gauge identifiers for 44 US
reservoirs in Texas, California, the Colorado River system and the Southeast,
plus two small helpers: place a level reading against full pool, and find the
agency page that publishes the live reading.

```python
import reservoir_fullpool as rf

rf.find("Lake Travis").full_pool_ft          # 681.0
rf.feet_from_full("Lake Travis", 677.23)     # -3.77  (3.77 ft below full)
rf.gauge_url("Lake Powell")                  # USGS NWIS page for site 09379900
rf.gauge_url("Shasta Lake")                  # CDEC station page for SHA
[r.name for r in rf.by_state("CA")]
```

```sh
python -m reservoir_fullpool "Lake Buchanan" 1012.4
```

## What is in the table

`slug, name, state, river, operator, full_pool_ft, capacity_af, live_data_feed, usgs_site, cdec_id`

* `usgs_site` values are USGS NWIS site numbers, checked on 2026-07-31 against the
  NWIS site service (every listed ID resolved to the named reservoir).
* `cdec_id` values are California Data Exchange Center station IDs.
* `full_pool_ft` and `capacity_af` are the operating agency's published
  conservation-pool figures, carried as published; cite the operator for them.
* Live levels are **not** bundled. They change daily; read them from the agency
  page that `gauge_url` returns, or from a site that tracks them, such as
  [LakeLevelNow's reservoir index](https://lakelevelnow.com/lakes/).

The useful part is the crosswalk: which gauge belongs to which named reservoir,
and who operates it. That mapping is otherwise scattered across LCRA, USACE,
USBR, IBWC and CDEC pages.

## License

Code MIT. The reservoir table is CC0 / public domain.
