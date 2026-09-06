
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


def get_all_tracts(years: list[int], us_state_codes: list[str], saveSpot: str | None = None) -> gpd.GeoDataFrame: 
  tract_years = []
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
        # tmp['state_code'] = us_state_code   # reproduces STUSPS
        tracts.append(tmp)
      except Exception as e: 
        print(f"Problem with {us_state_code}-{year}.")
    gdf_tracts = pd.concat(tracts, axis = 0)
    if saveSpot is not None:    # save each individual year, if desired. 
      gdf_tracts.to_file(f"{saveSpot}tracts_{year}.shp")
      print(f"Saved year {year}.")
    tract_years.append(gdf_tracts)
  gdf_tract_years = pd.concat(tract_years, axis = 0)
  return gdf_tract_years


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
  def __init__(self, geoid: str, crs: int = 3857, rings: int = 3, km: float = 1000.0) -> None:
    self.rings = rings
    self.geoid = geoid
    self.crs = crs
    self.km = km
  
  def get_rRing(self, gdf, verbose: bool = False) -> dict[list[int]]:
    
    # gdf = gdf
    # geoid = '25001015100'
    # km = 100
    # crs = 3857
    # rings = 3 
    
    pgdf = gdf.to_crs(self.crs)

    # clip to smaller region. 
    if self.km > 0: 
      pgdf = gpd.clip(pgdf, pgdf.loc[pgdf.GEOID == self.geoid, :].centroid.buffer(self.km * 1000))   
    queen = Queen.from_dataframe(pgdf, use_index = True)  # id_order preserves original index throughout (so, after clipping)
    
    r = 0
    ring_dict = {}
    while r < (self.rings + 1): 
      if r == 0: 
        idx = pgdf.loc[pgdf.GEOID == self.geoid, :].index.tolist()
        ring_dict['ring0'] = pgdf.loc[pgdf.GEOID == self.geoid, :].index.tolist()
      else: 
        idx = ring_dict[f'ring{r - 1}']
        ring_dict[f'ring{r}'] = [queen.neighbors[x] for x in idx][0]
      if verbose: 
        print(f'done with r = {r}.')
      r = r + 1
      self.rRing = ring_dict


year = 2024
us_2024 = get_all_tracts([year], us_state_codes)
# us_2024 = gpd.read_file(f"{saveSpot}tracts_{year}.shp")
ugh = Rings('25001015100') 
ugh.get_rRing(gdf = us_2024, verbose = True)
  
