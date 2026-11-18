"""Australian sources (GDA2020 and its MGA zones) are reprojected to EPSG:4326.

Layer import calls `IOConverter.to_parquet(..., target_crs="EPSG:4326")`; these
tests make the same call on a small GeoPackage written in each source CRS.
"""

from pathlib import Path

import duckdb
import pytest
from goatlib.io.converter import IOConverter

# Sydney Opera House, Perth CBD and Melbourne CBD as GDA2020 lon/lat, with the
# same points in their MGA zone.
CASES = [
    ("EPSG:7844", 151.2153, -33.8568, 151.2153, -33.8568),
    ("EPSG:7856", 334900.570, 6252288.753, 151.2153, -33.8568),
    ("EPSG:7850", 392307.203, 6464484.236, 115.8605, -31.9505),
    ("EPSG:7855", 320704.446, 5812911.700, 144.9631, -37.8136),
]


def _write_gpkg(path: Path, crs: str, x: float, y: float) -> Path:
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial")
    con.execute(
        f"COPY (SELECT 'site' AS name, ST_Point({x}, {y}) AS geom) TO '{path}' "
        f"WITH (FORMAT GDAL, DRIVER 'GPKG', SRS '{crs}')"
    )
    # Guard the premise: the file really declares the source CRS.
    col_type = con.execute(f"DESCRIBE SELECT geom FROM ST_Read('{path}')").fetchone()[1]
    assert col_type == f"GEOMETRY('{crs}')"
    return path


@pytest.mark.parametrize("crs,x,y,lon,lat", CASES, ids=[c[0] for c in CASES])
def test_gda2020_gpkg_is_reprojected_to_wgs84(
    tmp_path: Path, crs: str, x: float, y: float, lon: float, lat: float
) -> None:
    src = _write_gpkg(tmp_path / "gda2020.gpkg", crs, x, y)
    out = tmp_path / "out.parquet"

    meta = IOConverter().to_parquet(str(src), out, target_crs="EPSG:4326")

    assert meta.crs == "EPSG:4326"
    con = duckdb.connect()
    con.execute("LOAD spatial")
    got_x, got_y = con.execute(
        f"SELECT ST_X(geometry), ST_Y(geometry) FROM read_parquet('{out}')"
    ).fetchone()
    # Lon/lat order (not GDA2020's lat/lon axis order), within ~1 m.
    assert got_x == pytest.approx(lon, abs=1e-5)
    assert got_y == pytest.approx(lat, abs=1e-5)
