---
title: Loading, organizing, and calibrating 4D-STEM data
short_title: Data handling & calibration
---

:::{admonition} Hands-on tutorial
:class: important
- ▶️ [py4DSTEM basics: 4D-STEM data & Bragg disk detection](https://drive.google.com/file/d/13YClaGiPYZFIyKlHZNIqNVq-IWRGgiwm/view?usp=drive_link): load, browse, and virtually image a simulated polycrystalline Au dataset, then run your first disk detection.
:::

:::{admonition} Learning goals
:class: tip
- Load 4D-STEM data from vendor and open formats into an analysis-ready datacube.
- Browse a dataset interactively and read the standard summary views (mean/max pattern, virtual images).
- Apply the calibration chain: pixel sizes, origin/descan, elliptical distortion, and scan–detector rotation.
:::

Before any physics can come out of a 4D-STEM dataset, the data has to be loaded, organized, and, critically, calibrated. This module walks through the py4DSTEM data pipeline [](doi:10.1017/S1431927621000477): reading files, browsing the 4D datacube interactively, and applying the chain of calibrations that turn detector pixels into physical units.

## Loading data across formats

4D-STEM data arrives in many containers: vendor formats (Gatan `.dm4`, Thermo Fisher `.emd`/Velox, DECTRIS, Merlin/Medipix `.mib`, EMPAD raw), community HDF5 layouts (EMD 1.0), and plain arrays (`.npy`/`.npz`). py4DSTEM reads most of these directly, and any NumPy array can be wrapped into a `DataCube`:

```python
import py4DSTEM
datacube = py4DSTEM.import_file("experiment.dm4")

# or, from a raw array:
import numpy as np
data = np.load("scan.npz")["arr_0"]     # shape (Rx, Ry, Qx, Qy)
datacube = py4DSTEM.DataCube(data=data)
```

The four dimensions are conventionally ordered `(Rx, Ry, Qx, Qy)`: two real-space scan coordinates, then two reciprocal-space detector coordinates. Analysis products (mean patterns, virtual images, Bragg peaks, calibrations) are stored alongside the data in a tree structure that can be saved to and reloaded from HDF5, which also means expensive intermediate results (like Bragg disk detection over millions of patterns) can be checkpointed and shared.

## Browsing the datacube

The first thing to do with any new dataset is *look at it*. Scrubbing through diffraction patterns as a function of probe position builds intuition about what is in the data (where the vacuum is, which regions are crystalline, how much the pattern changes between neighboring positions) and immediately reveals problems like detector saturation or beam damage. The mean and maximum diffraction patterns computed over all probe positions give a compact overview of everything the detector saw:

:::{figure} ../assets/figures/dataset-overview.jpg
:alt: Standard summary views of a 4D-STEM dataset: vacuum probe, maximum diffraction pattern, Bragg vector map, simultaneous HAADF image, and Bragg peak histogram
:width: 100%
Standard first-look products for a 4D-STEM dataset: the vacuum probe, the maximum diffraction pattern over all positions, the Bragg vector map, the simultaneously recorded HAADF image, and the radial histogram of detected Bragg peaks.
:::

## The calibration chain

A useful mental model: every measurement we make in this course is a *position* or *intensity* in the diffraction pattern, so every distortion of the diffraction pattern propagates directly into the physics. The standard calibration chain is:

1. **Pixel sizes.** The real-space step size (from the scan settings) and the reciprocal-space pixel size (from the camera length, or better, measured from a known reference). Always sanity-check the scale bars on your virtual images afterwards.
2. **Origin / descan correction.** The center of the diffraction pattern shifts as the beam scans, due to imperfect descan alignment. A classic signature: the central disk in the *maximum* diffraction pattern looks like a rounded rectangle: the circular center disk convolved with the rectangle traced out by the descan across the scan. We measure the origin at every probe position and fit a smooth low-order surface to it, with robust fitting to suppress outliers.
3. **Elliptical distortion.** Projector lens distortions and detector tilt stretch the diffraction pattern into a slight ellipse. This can be measured from the amorphous halo of a carbon support film, or from a standard sample, and then corrected, or handled directly by working in polar-elliptical coordinates:

:::{figure} ../assets/figures/polar-elliptical.jpg
:alt: A diffraction pattern resampled in polar and polar-elliptical coordinates, with the elliptical transform straightening the rings
:width: 90%
Elliptical distortion in practice: resampling a ring pattern in plain polar coordinates leaves the rings wavy along the angular direction; including the fitted ellipticity straightens them, which sharpens every radial measurement downstream.
:::

4. **Real-space ↔ reciprocal-space rotation.** The scan direction and detector axes are rotated relative to each other (scan coils and camera each have their own orientation), and data can additionally be transposed on read-in. This rotation must be measured, for example with a center-of-mass (DPC-style) analysis of the center beam, where a correct rotation produces clean dipole contrast along x in CoMx and along y in CoMy. Getting this wrong rotates your strain tensor and orientation maps!
5. **Pixel size against a known structure.** For quantitative work, the reciprocal pixel size can be refined by comparing measured Bragg peak positions against structure factors calculated from a known reference crystal (e.g., from a CIF file).

:::{tip}
Record a vacuum probe image in every session. It provides the template for Bragg disk detection, measures the convergence angle, and captures the true probe shape. If you forget, a synthetic probe or a template extracted from a thin sample region can substitute, but it's never as good.
:::
