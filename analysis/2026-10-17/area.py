import numpy as np, json, sys
from affine import Affine
from scipy import ndimage
from pyproj import Transformer, Geod
G=Geod(ellps="WGS84")
d=np.load("crop.npz"); T=Affine(*json.load(open("T.json"))); fire=np.load("fire.npy")
nbr=(d["B5"]-d["B7"])/(d["B5"]+d["B7"])
tf=Transformer.from_crs(32612,4326,always_xy=True).transform
res={}
for thr in (0.06,0.08,0.10,0.12):
    m=ndimage.binary_opening(nbr<thr,iterations=1)|fire
    lab,n=ndimage.label(m,structure=np.ones((3,3)))
    keep=ndimage.binary_fill_holes(np.isin(lab,np.unique(lab[fire])))
    ii,jj=np.where(keep); xs,ys=T*(jj+0.5,ii+0.5)
    X=np.c_[xs-xs.mean(),ys-ys.mean()]; w,v=np.linalg.eigh(np.cov(X.T)); ax=v[:,1]; p=X@ax; q=X@v[:,0]
    a=[tf(xs[k],ys[k]) for k in (p.argmin(),p.argmax())]; sw=min(a,key=lambda t:t[1]); ne=max(a,key=lambda t:t[1])
    az,_,dd=G.inv(-110.9577,52.7678,*sw); az2,_,dd2=G.inv(-110.9577,52.7678,*ne)
    res[thr]=dict(area_ha=round(keep.sum()*0.09,1),length_m=round(float(p.max()-p.min())),width_m=round(float(np.percentile(q,98)-np.percentile(q,2))),axis_deg=round(float((np.degrees(np.arctan2(ax[0],ax[1]))+360)%180)),sw_tip=[round(x,5) for x in sw],sw_from_r11_m=round(dd),sw_bearing=round(az%360),ne_tip=[round(x,5) for x in ne],ne_from_r11_m=round(dd2))
    print(thr,res[thr])
    if thr==0.08: np.save("area1217.npy",keep)
json.dump(res,open("area1217.json","w"),indent=1)
