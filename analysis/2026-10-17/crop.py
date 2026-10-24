"""Landsat 8, Oct. 17, 2026, 18:17 UTC (12:17 p.m. MDT): active fire and burned area at CFB Wainwright.
Run from this folder, in order: crop.py (crop + calibrate to TOA reflectance / brightness temperature), fire.py (active-fire pixels,
Schroeder et al. 2016 thresholds, compared with NASA FIRMS), area.py (burned + burning area at 12:17 from the burn ratio, connected to fire pixels)."""
import rasterio, numpy as np, json
from rasterio.windows import from_bounds
from pyproj import Transformer
import os
U=os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../landsat/2026-10-17/LC08_L1TP_040023_20261017_20261021_02_T1/LC08_L1TP_040023_20261017_20261021_02_T1_")
F={b:b for b in ("B4","B5","B6","B7","B10")}
tf=Transformer.from_crs(4326,32612,always_xy=True).transform
x0,y0=tf(-111.02,52.72); x1,y1=tf(-110.80,52.83)
M={"B4":(2.0e-5,-0.1),"B5":(2e-5,-0.1),"B6":(2e-5,-0.1),"B7":(2e-5,-0.1)}
sun=26.57987682; out={}
for b,f in F.items():
    r=rasterio.open(U+f+".TIF"); w=from_bounds(x0,y0,x1,y1,r.transform); a=r.read(1,window=w).astype(float)
    if b in M: v=(a*M[b][0]+M[b][1])/np.sin(np.radians(sun))
    else:
        L=a*3.342e-4+0.1; v=1321.0789/np.log(774.8853/L+1)-273.15
    v[a==0]=np.nan; out[b]=v; T=r.window_transform(w)
    print(b,r.crs,r.res,a.shape,np.nanpercentile(v,[1,50,99,99.9]).round(3),np.nanmax(v).round(3))
np.savez("crop.npz",**out); json.dump(list(T)[:6],open("T.json","w"))
