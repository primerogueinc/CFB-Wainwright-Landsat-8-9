# How to view the Landsat files (without the grey screen)

The files in this repository are raw Landsat bands. Each `.TIF` holds **one band** of 16-bit numbers, not a picture. Opened on its own in a photo viewer, browser or Preview, it shows as flat grey or black. To see the fire you need to **stack three bands into one colour image and stretch the contrast**. This takes about ten minutes with QGIS, which is free.

**Just want to look?** Ready-made images are in `analysis/2026-10-17/` (`cfb-wainwright-landsat-1217.jpg`). The steps below are for checking our work yourself.

## What you need

- **QGIS**, free from [qgis.org](https://qgis.org) (Windows, Mac, Linux). The "Long Term Release" is fine.
- From `landsat/2026-10-17/LC08_L1TP_040023_20261017_20261021_02_T1/`: **B7, B6 and B5** (about 85 MB each). Download each `.TIF` with GitHub's "Download raw file" button.

## Steps

1. **Open QGIS** and start a new empty project.
2. **Add the three bands.** Drag `..._B7.TIF`, `..._B6.TIF` and `..._B5.TIF` into the QGIS window. They appear as three grey layers. That's normal.
3. **Stack them into one image.** Menu **Raster → Miscellaneous → Build Virtual Raster**.
   - **Input layers:** click the "…" button and tick B7, B6 and B5. Use the arrows so the order is **B7 first, then B6, then B5**.
   - Tick **"Place each input file into a separate band"**.
   - Click **Run**, then **Close**. A new layer called "Virtual" appears.
4. **Hide the grey layers.** Untick B7, B6 and B5 in the Layers panel and keep only "Virtual".
5. **Go to the base.** In the coordinate box at the bottom of the window, type **505400,5847350** and press Enter. Then set **Scale** (next to it) to **1:50000** and press Enter. The fire is the bright orange-yellow streak near the centre.
6. **Set the colours.** Right-click "Virtual" → **Properties** → **Symbology**:
   - **Render type:** Multiband color
   - **Red band:** Band 1 (B7). **Green band:** Band 2 (B6). **Blue band:** Band 3 (B5).
   - Open **Min / Max Value Settings**: choose **Cumulative count cut**, **2.0 %** to **98.0 %**; **Statistics extent: Updated canvas**; **Accuracy: Actual**.
   - Click **Apply**, then **OK**.
7. **Look.** Flames are bright orange to white; the strip they had already burned is darker; lakes are dark blue; cloud gives a soft haze. If the image is still dull, zoom in a little and press Apply in step 6 again: the contrast is recalculated for what's on screen.
8. **Save a picture (optional).** **Project → Import/Export → Export Map to Image.**

## Good to know

- **Why grey?** Landsat stores brightness as numbers from 0 to 65,535. Most of the ground uses a tiny slice of that range, so without a stretch everything looks the same shade.
- **Why these bands?** B7 and B6 are shortwave infrared, which sees flames through thin cloud and smoke. B5 is near infrared. Together (7-6-5) they show fire as orange or white against green-blue ground.
- **One band only?** Use **Singleband gray** with the same Cumulative count cut (2-98 %). B7 alone shows the fire as the brightest pixels.
- **Thermal (B10)** is a different kind of band. Its raw numbers need converting to temperature with the values in the `MTL.txt` file. We give the formula in `analysis/2026-10-17/crop.py`.
- **Oct. 16 (Landsat 9)** is 99.99% cloud, so expect mostly white.
- **Checking a file:** each folder's `manifest.json` lists the SHA-256 of every file, so you can confirm your download matches ours.

Prime Rogue Inc. · Landsat data courtesy of the U.S. Geological Survey · Questions or corrections: kevin@primerogueinc.com
