import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# --- Step 1: Load hazard polygons ---
hazard_gdf = gpd.read_file("./Tubajon Maps/Soil Erosion/Soil Erosion.shp")  # your hazard shapefile
# Ensure it has 'Hazard' and 'HazardRisk' columns

# --- Step 2: Load building points ---
buildings_df = pd.read_csv("./inputs/buildings.csv")  # with BuildingCode, Latitude, Longitude

# Convert to GeoDataFrame
buildings_gdf = gpd.GeoDataFrame(
    buildings_df,
    geometry=[Point(xy) for xy in zip(buildings_df.Longitude, buildings_df.Latitude)],
    crs="EPSG:4326"  # Assuming WGS84 for lat/lon
)

# --- Step 3: Match CRS ---
# Reproject buildings to match hazard CRS if different
if buildings_gdf.crs != hazard_gdf.crs:
    buildings_gdf = buildings_gdf.to_crs(hazard_gdf.crs)

# --- Step 4: Spatial join ---
joined_gdf = gpd.sjoin(
    buildings_gdf,
    hazard_gdf[['Hazard', 'HazardRisk', 'geometry']],
    how='left',
    predicate='intersects'
)

# --- Step 5: Keep only rows with hazard info ---
# Drop rows where HazardRisk is missing (NaN)
joined_gdf = joined_gdf.dropna(subset=['HazardRisk'])

# --- Step 6: Select only desired columns ---
final_df = joined_gdf[['BuildingCode', 'Hazard', 'HazardRisk']]

# --- Step 7: Export result ---
final_df.to_csv("building_hazard.csv", index=False)

print("Done! Output saved to building_hazard.csv")