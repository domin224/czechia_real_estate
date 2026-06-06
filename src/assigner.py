"""Assign RÚIAN municipality codes to scraped real estate listings.

This script performs a spatial join between scraped property listings (which
contain GPS coordinates) and municipality polygons from the Czech RÚIAN
register. Each listing is enriched with the municipality name, municipality
code and the NUTS/LAU code of the area it falls into.

Example
-------
    python src/assigner.py \\
        --input reality_houses.csv \\
        --municipalities obce_polygony.geojson \\
        --output input_with_ruian.csv
"""

import argparse

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


def assign_ruian(input_path: str, municipalities_path: str, output_path: str) -> None:
    """Enrich listings with municipality and NUTS/LAU codes via a spatial join.

    Parameters
    ----------
    input_path:
        CSV file with the scraped listings. Must contain ``longitude`` and
        ``latitude`` columns in WGS84 (EPSG:4326).
    municipalities_path:
        GeoJSON (or any GeoPandas-readable file) with municipality polygons.
        Expected attribute columns: ``Nazev``, ``Kod`` and ``NutsLau``.
    output_path:
        Destination CSV file for the enriched listings.
    """
    # 1. Load listings and build point geometries from the GPS coordinates.
    df = pd.read_csv(input_path)
    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
    gdf_points = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    # 2. Load municipality polygons and align the coordinate reference system.
    gdf_municipalities = gpd.read_file(municipalities_path)
    if gdf_municipalities.crs is not None and gdf_municipalities.crs != gdf_points.crs:
        gdf_municipalities = gdf_municipalities.to_crs(gdf_points.crs)

    # 3. Spatial join: match each listing to the municipality it lies within.
    gdf_joined = gpd.sjoin(
        gdf_points,
        gdf_municipalities,
        how="left",
        predicate="intersects",
    )
    gdf_joined = gdf_joined.rename(
        columns={
            "Nazev": "Obec_nazev",
            "Kod": "Obec_kod",
            "NutsLau": "NutsLau",
        }
    )

    # 4. Save only the original columns plus the newly assigned RÚIAN attributes.
    columns_to_save = list(df.columns) + ["Obec_nazev", "Obec_kod", "NutsLau"]
    gdf_joined[columns_to_save].to_csv(output_path, index=False)
    print(f"Saved {len(gdf_joined)} enriched listings to {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default="reality_houses.csv",
        help="Input CSV with scraped listings (default: reality_houses.csv)",
    )
    parser.add_argument(
        "--municipalities",
        default="obce_polygony.geojson",
        help="GeoJSON with municipality polygons (default: obce_polygony.geojson)",
    )
    parser.add_argument(
        "--output",
        default="input_with_ruian.csv",
        help="Output CSV path (default: input_with_ruian.csv)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    assign_ruian(args.input, args.municipalities, args.output)
