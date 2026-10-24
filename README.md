# CFB Wainwright fire: Landsat 8-9 raw files

Raw, unmodified Landsat Collection 2 band files from USGS EarthExplorer for the Oct. 17, 2026 fire at CFB Wainwright, Alberta, kept so anyone can check the analysis in the [CFB Wainwright fire archive](https://github.com/primerogueinc/cfb-wainwright-fire-archive).

## Scenes

| Date (UTC) | Product ID | Time | Files | Note |
|---|---|---|---|---|
| 2026-10-17 | LC08_L1TP_040023_20261017_20261021_02_T1 | 18:17 UTC (12:17 p.m. MDT) | B4, B5, B6, B7, B10, MTL (txt, xml), ANG | **The only close-up of the fire while it burned.** Scene cloud cover 83%: thin, cold cloud over the base, but flames show through in the shortwave infrared. |

Folder: `landsat/<date UTC>/<product ID>/`, files named as in the product's MTL file. `manifest.json` gives the SHA-256 of each file and the name it arrived under.

## Oct. 17, 12:17 p.m.: what it shows

Scripts and outputs: `analysis/2026-10-17/` (`crop.py`, `fire.py`, `area.py`; graphic `cfb-wainwright-landsat-1217.jpg`).

- **34 active-fire pixels** (30 m) by the Schroeder et al. (2016) thresholds (B7/B5 > 2.5, B7 − B5 > 0.3, B7 > 0.5); 47 of NASA FIRMS' 59 detections from this pass fall within 45 m of them. List: `landsat_fire_pixels_20261017_1817utc.csv`.
- **Burned and burning area at 12:17 p.m.:** a strip about 2.0-2.3 km long and 0.26-0.37 km wide, axis ~55-58° (pushed northeast by a southwest wind), 26-71 ha depending on the burn-ratio threshold (`area1217.json`). Its back (southwest) end lies **1.2-1.5 km east of Range 11, bearing 78-82°**: inside the C16's ~2.2 km reach and the range's inferred firing sector.
- **No heat at the gas lines.** Within 600 m of every operating gas line (AER licence data), band 7 and the B7/B5 ratio are at background (max ratio 0.8; fire pixels ≥ 2.5). The nearest flames were 0.86 km from a gas line, 0.87 km from the Range 2 point and 1.34 km from the road head.

Limits: thin cloud lowers the signal; the burned-area outline depends on the threshold (range given); pixel positions are good to about one 30 m pixel.

## Adding files

```
python3 scripts/ingest.py path/to/LC08_..._B7.TIF [more files]
```

## Licence

Scripts and documentation: CC BY-NC 4.0 (Prime Rogue Inc.). Data: Landsat imagery courtesy of the U.S. Geological Survey; public domain.
