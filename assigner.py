import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# === CONFIGURATION ===
CSV_PATH = '/Users/dominiksvab/Documents/projekt_nemovitosti/reality_houses.csv'  # Path to your CSV file
OUTPUT_PATH = 'input_with_ruian.csv'  # Output CSV file
GDF_OBCE_PATH = '/Users/dominiksvab/Documents/projekt_nemovitosti/obce_polygony.geojson'

# 1. Načti body z CSV
df = pd.read_csv(CSV_PATH)
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
gdf_points = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# 2. Načti polygony obcí
gdf_obce = gpd.read_file(GDF_OBCE_PATH)

# 3. Prostorový join: obce
gdf_joined = gpd.sjoin(
    gdf_points,
    gdf_obce,
    how="left",
    predicate='intersects'
)
gdf_joined = gdf_joined.rename(columns={
    'Nazev': 'Obec_nazev',
    'Kod': 'Obec_kod',
    'NutsLau': 'NutsLau'
})

# 4. Ulož výsledek
columns_to_save = list(df.columns) + [
    'Obec_nazev', 'Obec_kod', 'NutsLau'
]
gdf_joined[columns_to_save].to_csv(OUTPUT_PATH, index=False)