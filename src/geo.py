
import numpy as np
import pandas as pd 
import geopandas as gpd
import libpysal
import pygris
import matplotlib.pyplot as plt

saveSpot = '/Users/Jason/Documents/Machine Learning/gen_ai/tracts/'


us_state_codes = [
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", 
    "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", 
    "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", 
    "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", 
    "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"
]

years = [1990, 2000] + list(range(2010, 2026)) #list(range(2000, 2030))



for year in years: 
  tracts = []
  print(f"Starting {year}...")
  for us_state_code in us_state_codes: 
    try: 
      try: 
        tmp = pygris.tracts(state = us_state_code, year = year, cb = True)
        tmp['cb'] = True
      except Exception as e: 
        tmp = pygris.tracts(state = us_state_code, year = year, cb = False)
        tmp['cb'] = False
      tmp['year'] = year
      tmp['state_code'] = us_state_code 
      tracts.append(tmp)
    except Exception as e: 
      print(f"Problem with {us_state_code}-{year}.")
  df_tracts = pd.concat(tracts, axis = 0)
  df_tracts.to_file(f"{saveSpot}tracts_{year}.shp")
  print(f"Saved year {year}.")

  
year = 2022
gdf = gpd.read_file(f"{saveSpot}tracts_{year}.shp")

# a function to create a tract-based plot. 
def plot_tracts(geoid: str): 
  # geoid = '25001015100'
  

# defining arguments for __init__ sets up object configuration.  this gives the required 
#   inputs to initialize a specific instance of the class.  it allows passing unique data.
#   it executes every single time it instantiates.  
# defining arguments in class name sets up inheritance.  this tells python that the class 
#   is a child class that should inherit all the methods and attributes of the parent class 
#   in the parentheses.  it runs exactly once when python first reads it.  this helps to 
#   build standard class hierarchies.  

from libpysal.weights import Queen 

# def __init__ always returns None. 
class Rings: 
  def __init__(self, geoid: str, crs: int = 3857, rings: int = 3) -> None:
    self.rings = rings
    self.geoid = geoid
    self.crs = crs
    
  def get_0ring(self) -> gpd.GeoSeries: 
    """Identify 0-ring polygon of provided geoid."""
    pgdf = gdf.to_crs(self.crs)
    self.ring0 = pgdf.loc[pgdf.GEOID == self.geoid, 'geometry']
    # return ring0
  
  def get_rRing(self, r: int) -> gpd.GeoSeries: # blah
    """Identify 1-ring to R-ring polygons of provided geoid."""
    try: 
      self.ringr = Queen.from_dataframe(self.ring0)
    except AttributeError: 
      self.get_0ring(self)
      self.ringr = Queen.from_dataframe(self.ring0)
      
  def rings_function(gdf, geoid, crs, km: int = 0, rings: int = 3):
    
    # gdf = gdf
    # geoid = '25001015100'
    # km = 100
    # crs = 3857
    # rings = 3 
    
    pgdf = gdf.to_crs(crs)

    # clip to smaller region. 
    if km > 0: 
      pgdf = gpd.clip(pgdf, pgdf.loc[pgdf.GEOID == geoid, :].centroid.buffer(km * 1000))   
    queen = Queen.from_dataframe(pgdf, use_index = True)  # id_order preserves original index throughout (so, after clipping)
    
    r = 0
    ring_dict = {}
    while r < (rings + 1): 
      
      if r == 0: 
        idx = pgdf.loc[pgdf.GEOID == geoid, :].index.tolist()
        ring_dict['ring0'] = pgdf.loc[pgdf.GEOID == geoid, :].index.tolist()
      else: 
        idx = ring_dict[f'ring{r - 1}']
        ring_dict[f'ring{r}'] = [queen.neighbors[x] for x in idx][0]
      print(f'done with r = {r}.')
      r = r + 1
    return ring_dict
    
  
def rings_function(gdf, geoid, crs, km: int = 0, rings: int = 3):
  
  # gdf = gdf
  # geoid = '25001015100'
  # km = 100
  # crs = 3857
  # rings = 3 
  
  pgdf = gdf.to_crs(crs)

  # clip to smaller region. 
  if km > 0: 
    pgdf = gpd.clip(pgdf, pgdf.loc[pgdf.GEOID == geoid, :].centroid.buffer(km * 1000))   
  queen = Queen.from_dataframe(pgdf, use_index = True)  # id_order preserves original index throughout (so, after clipping)
  
  r = 0
  ring_dict = {}
  while r < (rings + 1): 
    
    if r == 0: 
      idx = pgdf.loc[pgdf.GEOID == geoid, :].index.tolist()
      ring_dict['ring0'] = pgdf.loc[pgdf.GEOID == geoid, :].index.tolist()
    else: 
      idx = ring_dict[f'ring{r - 1}']
      ring_dict[f'ring{r}'] = [queen.neighbors[x] for x in idx][0]
    print(f'done with r = {r}.')
    r = r + 1
  return ring_dict
    
ugh = rings_function(gdf, '25001015100', 3857)#, 3)
    
    
    
boo = Queen.from_dataframe(pgdf)
boo.neighbors[the_geoid_index]



    
  if r == (rings + 1):
    return base_value
  
  # recursive case.  function calls itself with modfied parameters
  else: 
    return recursive_function(gdf)
    
    
ugh = Rings('25001015100')

ugh.get_0ring().plot(color = 'skyblue', edgecolor = 'black')


# 3. Select your "given polygon" (e.g., the first row in the GeoDataFrame)
given_polygon = gdf.iloc[0]['geometry']

# 4. Get the centroid of the given polygon
centroid = given_polygon.centroid

# 5. Create a 30 km (30,000 meters) buffer around the centroid
buffer_30km = centroid.buffer(30000)

# 6. Find all polygons in the GeoDataFrame that intersect with this buffer
intersecting_polygons = gdf[gdf.intersects(buffer_30km)]

# Optional: View the results
print(intersecting_polygons)
  
  
  
  # Build a Queen contiguity weights object (shares edge or vertex)
  wq = libpysal.weights.Queen.from_dataframe(gdf)

# Get neighbors for a specific polygon index, e.g., index 0
neighbors_of_zero = wq.neighbors[0]
print(neighbors_of_zero)
  
  # 0-ring
  gdf.loc[gdf.GEOID == geoid]
  
  
  
import json
import os
import pandas as pd
import plotly.express as px
import requests
from pydantic_ai import Agent, RunContext



def generate_tract_choropleth(state_name: str) -> str:
    """Fetches Census data and tract boundaries to display an interactive plotly map."""
    state_clean = state_name.lower().strip()
    fips = STATE_FIPS.get(state_clean)

    if not fips:
        return fips_error_handling(state_name)

    # 1. Fetch live 2022 ACS 5-Year Estimate Median Income (Variable B19013_001E)
    # Docs: https://census.gov
    census_url = f"https://census.gov:{fips}"
    response = requests.get(census_url)

    if response.status_code != 200:
        return f"Error connecting to the Census API: {response.text}"

    # Parse Census data into a DataFrame
    raw_data = response.json()
    df = pd.DataFrame(raw_data[1:], columns=raw_data[0])
    df["Median Income"] = pd.to_numeric(df["B19013_001E"], errors="coerce")

    # Construct the unique GEOID string to match the geojson format
    df["GEOID"] = df["state"] + df["county"] + df["tract"]

    # Drop missing values for clean color mapping
    df = df.dropna(subset=["Median Income"])
    df = df[df["Median Income"] > 0]  # Filter out negative placeholder values

    # 2. Grab boundaries dynamically via US Census Bureau GeoJSON API
    # TIGERweb REST API documentation: https://census.gov
    geojson_url = f"https://census.gov{fips}%27&outFields=GEOID&f=geojson"

    try:
        gdf = gpd.read_file(geojson_url)
    except Exception as e:
        return f"Failed to download tract geometries: {str(e)}"

    # 3. Merge tabular data and geometry
    merged = gdf.merge(df, on="GEOID")

    # 4. Generate Interactive Plotly Mapbox Figure
    # We use a sample of tracts if the state is massive to avoid memory bloating
    if len(merged) > 2000:
        merged = merged.sample(n=2000, random_state=42)

    merged = merged.to_crs(epsg=4326)

    fig = px.choropleth_mapbox(
        merged,
        geojson=json.loads(merged.to_json()),
        locations=merged.index,
        color="Median Income",
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": merged.geometry.centroid.y.mean(), "lon": merged.geometry.centroid.x.mean()},
        opacity=0.6,
        labels={"Median Income": "Median Household Income ($)"},
        title=f"Census Tract Choropleth: Median Household Income in {state_name.title()}",
    )
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})

    # Save visualization to a local HTML file and return it
    output_filename = f"{state_clean}_income_map.html"
    fig.write_html(output_filename)

    return f"Success! Generated the interactive choropleth. Saved directly to `{output_filename}`. Open this file in a web browser to view the interactive map."


def fips_error_handling(state_name: str) -> str:
    return f"Sorry, I don't have the FIPS code configured for '{state_name}'. Please try California, Texas, New York, or Florida."
