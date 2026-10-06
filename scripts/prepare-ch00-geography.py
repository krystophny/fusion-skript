"""Fetch native-resolution Sentinel TCI windows and normalize map coordinates.
Run: uv run --python 3.13 --with rasterio --with pyproj --with pillow \
  --with shapely --with matplotlib python scripts/prepare-ch00-geography.py
No credentials, styling decisions, or OSM-derived data are used.
"""
import json
from pathlib import Path
import numpy as np
import rasterio
from rasterio.windows import from_bounds
from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/ch00/raw'
OUT = ROOT / 'data/ch00/processed'
PHOTOS = ROOT / 'slides/photos'
CHECK = ROOT / 'derivations/build/check'


def build():
    for p in [OUT, PHOTOS / 'originals', CHECK]:
        p.mkdir(parents=True, exist_ok=True)
    scene = json.loads((RAW / 'sentinel_selected.json').read_text())
    url = scene['assets']['visual']['href']
    project = Transformer.from_crs(4326, 32633, always_xy=True)
    park_x, park_y = project.transform(13.686692, 52.650568)
    boundary = json.loads((RAW / 'graz_boundary.geojson').read_text())
    city = transform(project.transform, shape(boundary['features'][0]['geometry']))
    center_x, center_y = city.centroid.x, city.centroid.y
    local = transform(lambda x, y, z=None: (np.asarray(x)-center_x,
                                           np.asarray(y)-center_y), city)
    (OUT / 'graz-outline-metres.geojson').write_text(json.dumps({
        'type': 'FeatureCollection', 'features': [{'type': 'Feature',
        'properties': {'units': 'm', 'crs': 'local offset of EPSG:32633',
                       'origin_easting_m': center_x, 'origin_northing_m': center_y},
        'geometry': mapping(local)}]}, indent=2))
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR',
                      AWS_NO_SIGN_REQUEST='YES'):
        with rasterio.open(url) as ds:
            assert ds.crs.to_epsg() == 32633
            for size, name in [(16000, 'weesow-sentinel-same-scale'),
                               (5000, 'weesow-sentinel-detail')]:
                win = from_bounds(park_x-size/2, park_y-size/2,
                                  park_x+size/2, park_y+size/2, ds.transform)
                win = win.round_offsets().round_lengths()
                assert 0 <= win.col_off and 0 <= win.row_off
                assert win.col_off+win.width <= ds.width
                assert win.row_off+win.height <= ds.height
                array = ds.read(window=win)
                profile = ds.profile.copy()
                profile.update(width=array.shape[2], height=array.shape[1],
                               transform=ds.window_transform(win), driver='GTiff')
                with rasterio.open(PHOTOS/'originals'/f'{name}.tif','w',**profile) as dest:
                    dest.write(array)
                im = Image.fromarray(array.transpose(1,2,0))
                im.save(PHOTOS/'originals'/f'{name}.jpg', quality=98)
                im.thumbnail((2400,2400)); im.save(PHOTOS/f'{name}.jpg', quality=92)
                if size == 16000:
                    image_array = array.transpose(1,2,0)
                    bounds = rasterio.windows.bounds(win, ds.transform)
                    extent = [bounds[0]-park_x, bounds[2]-park_x,
                              bounds[1]-park_y, bounds[3]-park_y]
    metadata = {'park': 'Weesow-Willmersdorf', 'park_coordinates_wgs84':
                {'latitude':52.650568,'longitude':13.686692},
                'coordinate_source':'https://www.wikidata.org/wiki/Q71147169',
                'scene_id':scene['id'], 'datetime':scene['properties']['datetime'],
                'source_url':url, 'resolution_m':10,
                'map_extent_relative_to_park_m':extent,
                'graz_projected_area_km2':city.area/1e6,
                'graz_published_area_km2':127.58,
                'map_crs':'EPSG:32633', 'graz_origin_m':[center_x,center_y],
                'credit':'Contains modified Copernicus Sentinel data 2025; '
                         'Datenquelle: Stadt Graz – data.graz.gv.at',
                'licence_url':'https://cds.climate.copernicus.eu/licences/ec-sentinel',
                'boundary_licence':'CC BY 4.0',
                'boundary_terms':'https://data.graz.gv.at/graz/nutzungsbedingungen/',
                'modifications':'Native 10 m TCI window; boundary projected and translated. '
                                'Same metre axes, equal aspect; no map screenshots.'}
    (OUT/'geography.json').write_text(json.dumps(metadata, indent=2))
    fig, axes = plt.subplots(1,2,figsize=(10,5), layout='constrained')
    axes[0].imshow(image_array, extent=np.array(extent)/1000)
    axes[0].set_title('Weesow-Willmersdorf (16 km window)')
    for geom in ([local] if local.geom_type=='Polygon' else local.geoms):
        x,y=geom.exterior.xy;axes[1].plot(np.asarray(x)/1000,np.asarray(y)/1000,'k-')
    axes[1].set_title('Graz city boundary')
    for ax in axes:
        ax.set(xlim=(-8,8),ylim=(-8,8),xlabel='East [km]',ylabel='North [km]')
        ax.set_aspect('equal')
    fig.savefig(CHECK/'08-same-scale.png',dpi=150);plt.close(fig)
    print(json.dumps({'scene':metadata['scene_id'],'graz_area_km2':city.area/1e6,
                      'native_window_pixels':list(image_array.shape[:2])}))

if __name__ == '__main__':
    build()
