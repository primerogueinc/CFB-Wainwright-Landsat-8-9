import os, numpy as np, json, pandas as pd
from affine import Affine
from pyproj import Transformer
from scipy import ndimage
d=np.load("crop.npz"); T=Affine(*json.load(open("T.json")))
r5,r6,r7=d["B5"],d["B6"],d["B7"]; R75=r7/r5
una=(R75>2.5)&((r7-r5)>0.3)&(r7>0.5)
cand=(R75>1.8)&((r7-r5)>0.17)
# contextual for candidates: R75 > mean+3sd in 61x61 window of non-candidates
bg=np.where(cand,np.nan,R75)
k=61
mu=ndimage.generic_filter(np.nan_to_num(bg,nan=np.nanmean(bg)),np.mean,size=k,mode='nearest')
sd=ndimage.generic_filter(np.nan_to_num(bg,nan=np.nanmean(bg)),np.std,size=k,mode='nearest')
ctx=cand&(R75>mu+3*np.maximum(sd,0.8))&(r7>r7.mean()+3*max(r7.std(),0.08))
fire=una|ctx
print("unambiguous",una.sum(),"contextual",ctx.sum(),"fire px",fire.sum(),"area ha",fire.sum()*0.09)
ii,jj=np.where(fire); xs,ys=T*(jj+0.5,ii+0.5)
tf=Transformer.from_crs(32612,4326,always_xy=True).transform
lo,la=tf(xs,ys)
df=pd.DataFrame(dict(lon=lo,lat=la,r7=r7[ii,jj],r6=r6[ii,jj],r5=r5[ii,jj],R75=R75[ii,jj],unambiguous=una[ii,jj]))
df.to_csv("landsat_fire_pixels_20261017_1817utc.csv",index=False)
print(df.describe().round(4).to_string())
f=pd.read_csv(os.environ.get("FIRMS_CSV","../../../cfb-wainwright-fire-archive/data/firms/detections.csv")); L=f[f.acq_datetime_mdt=="2026-10-17 12:17 MDT"]
print("FIRMS 12:17 n",len(L), L.columns.tolist()[:12])
# match: FIRMS points within 45 m of our fire pixels
from scipy.spatial import cKDTree
fx,fy=Transformer.from_crs(4326,32612,always_xy=True).transform(L.longitude.values,L.latitude.values)
t=cKDTree(np.c_[xs,ys]); dd,_=t.query(np.c_[fx,fy]); print("FIRMS matched within 45 m:",(dd<45).sum(),"median dist",np.median(dd).round(1))
lab,n=ndimage.label(fire,structure=np.ones((3,3))); print("clusters",n,"sizes",sorted(ndimage.sum(fire,lab,range(1,n+1)).astype(int).tolist(),reverse=True)[:10])
np.save("fire.npy",fire)
