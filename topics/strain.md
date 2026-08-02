---
title: Strain mapping with nanobeam electron diffraction
short_title: Strain mapping
---

:::{admonition} Hands-on tutorial
:class: important
- ▶️ [Strain mapping of a partially cycled LiFePO₄ battery cathode](https://drive.google.com/file/d/1aQaRR-XZzCZayfYsSDVuz7prLeolsVKI/view?usp=drive_link): the full workflow from vacuum probe to strain maps, including the descan, ellipticity, and rotation calibrations.
:::

:::{admonition} Learning goals
:class: tip
- Run the full strain-mapping workflow: probe template → Bragg disk detection → calibration → lattice fitting → strain maps.
- Choose detection hyperparameters and a reference lattice, and understand how each choice shapes the result.
- Know the main precision limits (disk edge sharpness, thickness effects, calibration errors) and how to mitigate them.
:::

```{image} ../assets/cover-strain.jpg
:alt: Schematic of nanobeam strain mapping: a converged probe scanned over a strained crystal produces diffraction patterns whose Bragg disk positions encode the local lattice vectors
:width: 100%
```

Strain, the local deviation of the lattice from its relaxed spacing, controls band structure in semiconductor devices, mobility in strained channels, ferroelastic domain patterns, and mechanical response around defects and precipitates. Nanobeam electron diffraction (NBED) strain mapping [](doi:10.1063/1.4922994) measures it directly: the positions of the Bragg disks in each diffraction pattern encode the local reciprocal lattice vectors, so tracking how disk positions shift as the probe scans across the sample gives the full 2D strain tensor (ε<sub>xx</sub>, ε<sub>yy</sub>, ε<sub>xy</sub>, and lattice rotation θ) at every probe position, over fields of view of microns with nanometer resolution. Among the many strain-measurement techniques in the TEM [](doi:10.1016/j.ultramic.2013.03.014), including geometric phase analysis of high-resolution images [](doi:10.1016/S0304-3991(98)00035-7), NBED stands out for combining large fields of view, high precision, and modest dose.

## How it works

1. **Probe template.** Record a vacuum probe image (or extract a template from a thin region of the dataset). Its cross-correlation kernel, typically shaped with a sigmoid edge, is what makes disk detection precise.
2. **Bragg disk detection.** Cross-correlate the template with every diffraction pattern and locate the correlation maxima with subpixel precision [](doi:10.1016/j.ultramic.2016.12.021). The key hyperparameters are the correlation power, minimum peak intensity/spacing, and the subpixel mode (`'poly'` is fast for tutorials; **`'multicorr'` is recommended for high-precision strain mapping**). Always tune the detection parameters on a handful of test patterns before running the full scan.
3. **Calibration.** Correct the origin (descan), elliptical distortion, and the real-space/reciprocal-space rotation; see the [data handling module](./data-handling.md). Calibration errors map directly into artificial strain.
4. **Lattice fitting.** Choose basis vectors *g*₁ and *g*₂ from the Bragg vector map (ideally perpendicular, well-separated reflections), and fit the full lattice at every probe position.
5. **Strain from a reference.** Strain is always measured *relative to a reference lattice*: either the median lattice over a region of interest known to be unstrained, or manually specified reference vectors. The transformation between the local and reference lattice vectors, rotated into your chosen coordinate system, gives ε<sub>xx</sub>, ε<sub>yy</sub>, ε<sub>xy</sub>, and θ.

:::{figure} ../assets/figures/strain-maps.jpg
:alt: Mean diffraction pattern with fitted lattice, and resulting strain component maps of a multilayer film
:width: 100%
A complete result: the mean diffraction pattern with the fitted reciprocal lattice, and the four strain-tensor component maps (ε<sub>xx</sub>, ε<sub>yy</sub>, ε<sub>xy</sub>, θ) across a multilayer structure.
:::

## Precision and pitfalls

- Disk registration precision improves with sharp, uniform disk edges; this is where convergence angle, sample thickness (dynamical contrast inside the disks), and patterned probes matter. Precision of ~10⁻⁴ relative strain is achievable in favorable cases; a few ×10⁻³ is routine.
- Thickness and mistilt vary across real samples and modulate the intensity *inside* disks, which can bias center-fitting; robust registration algorithms and (where available) precession [](doi:10.1107/S2052252514022283) help. Precession-assisted acquisition markedly narrows the strain error distribution.

:::{figure} ../assets/figures/maped-strain.jpg
:alt: Conventional versus precession-averaged diffraction patterns and the corresponding strain maps, showing reduced artifacts with precession
:width: 100%
Conventional (top) vs. precession/multi-beam-averaged (bottom) acquisition of the same region: averaging through the rocking condition suppresses the dynamical intensity variations inside the disks, and the strain maps get visibly cleaner.
:::

- **Patterned "bullseye" probes** (apertures with concentric rings or radial spokes milled into the condenser aperture) imprint sharp internal structure onto every Bragg disk, improving registration precision severalfold at fixed dose [](doi:10.1016/j.ultramic.2019.112890):

:::{figure} ../assets/figures/bullseye-apertures.jpg
:alt: Focused-ion-beam-fabricated bullseye condenser apertures
:width: 60%
Bullseye and patterned condenser apertures fabricated with a focused ion beam. Installed in the condenser system, they shape every diffraction disk into a self-registering target.
:::

:::{figure} ../assets/figures/bullseye-detection.jpg
:alt: Bullseye probe template and detected diffraction disks in an experimental pattern
:width: 90%
Disk detection with a bullseye probe: the patterned template cross-correlates sharply against each reflection, even where diffraction contrast varies across the disk.
:::

- The choice of reference region is a physics decision, not a software one: strain maps are only as meaningful as the reference lattice they are measured against.
- Useful derived quantities: the *strain dilation* ε<sub>xx</sub> + ε<sub>yy</sub> (volumetric part), and statistics of strain over segmented regions, for example comparing precipitates against the surrounding matrix in irradiated alloys [](doi:10.1016/j.actamat.2025.121095).
