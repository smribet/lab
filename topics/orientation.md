---
title: Automated crystal orientation and phase mapping
short_title: Orientation & phase mapping
---

:::{admonition} Hands-on tutorial
:class: important
- ▶️ [Phase, orientation & strain of a two-phase Ti alloy](https://drive.google.com/file/d/1_DaUuEqq5vx_1ZM5R7zChEo7iA_ccprC/view?usp=drive_link): ACOM for the α and β phases, phase quantification, and strain extracted directly from the matched patterns.
:::

:::{admonition} Learning goals
:class: tip
- Build an orientation plan from a reference crystal structure and match it to experimental Bragg peaks.
- Generate and interpret orientation maps, correlation-score maps, and phase maps.
- Understand why precession improves pattern quality and matching reliability.
:::

```{image} ../assets/cover-orientation.jpg
:alt: Schematic of automated crystal orientation mapping: diffraction patterns from a polycrystalline film are matched against a library of simulated patterns over all orientations
:width: 100%
```

Most functional and structural materials are polycrystalline, and their properties depend on grain size, texture, grain boundary character, and phase distribution. Automated crystal orientation mapping (ACOM) in 4D-STEM [](doi:10.1016/j.matchar.2014.08.010) measures all of these: at every probe position, the recorded diffraction pattern is matched against a library of patterns simulated over all possible crystal orientations, and the best match assigns a local orientation, similar to electron backscatter diffraction (EBSD) in the SEM but in transmission, with nanometer resolution, and on the same datasets used for every other analysis in this course.

## How it works

1. **Reference structures.** Load the candidate crystal structures (e.g., from CIF files) and compute their structure factors up to the maximum scattering vector recorded on the detector.
2. **Orientation plan.** Simulate diffraction patterns over a grid of orientations covering the symmetry-reduced zone axis range: a lookup table of expected Bragg peak positions and intensities. Grid spacings of a few degrees, with local refinement, balance accuracy against speed.
3. **Bragg peak detection.** As for strain mapping, detect the diffraction peaks at every probe position (the same calibrated Bragg vectors feed both analyses).
4. **Correlation matching.** For each probe position, score the measured peaks against the orientation library [](doi:10.1017/S1431927622000101) and keep the best match(es). Returning multiple matches with a minimum angular separation handles overlapping grains along the beam direction.
5. **Orientation and phase maps.** The result is an orientation map (typically displayed with inverse-pole-figure coloring for in-plane and out-of-plane directions), plus per-position correlation scores. Running plans for multiple candidate phases and comparing their correlation scores produces a **phase map**, along with quantitative phase-fraction estimates.

## Precession and pattern quality

Zone-axis nanobeam patterns are strongly dynamical: intensities oscillate with thickness and small mistilts, which degrades matching against kinematical templates. **Precession electron diffraction (PED)** [](doi:10.1107/S2052252514022283), which rocks the beam on a cone (typically ~0.3–1°) while descanning below the sample, integrates through the rocking curve and produces more kinematical-like, more complete patterns:

:::{figure} ../assets/figures/precession-patterns.png
:alt: Diffraction patterns acquired with increasing beam-rocking radius, showing more complete and uniform Bragg spot intensities
:width: 100%
The effect of precession: as the rocking radius increases, more reflections are excited and their intensities become more uniform, much closer to the kinematical patterns the orientation library assumes.
:::

Precession substantially improves both orientation reliability and phase discrimination, and the tutorial dataset for this module is a precession 4D-STEM measurement of a two-phase (α + β) titanium alloy [](doi:10.1111/jmi.13275), archived openly at the [University of Glasgow research data repository](https://doi.org/10.5525/gla.researchdata.1514).

## Phase mapping in hard cases

Phase discrimination gets genuinely difficult when the candidate structures are closely related: polymorphs sharing a parent lattice, with only subtle differences in symmetry and spacing. Ferroelectric hafnium zirconium oxide (HZO) is a canonical example:

:::{figure} ../assets/figures/hzo-polymorphs.jpg
:alt: Crystal structures of the monoclinic, tetragonal, and orthorhombic polymorphs of hafnium zirconium oxide
:width: 100%
The HZO polymorph problem: monoclinic, tetragonal, and two orthorhombic phases (one of them the ferroelectric structure) differ only slightly in lattice parameters and symmetry, a stringent test for diffraction-based phase mapping.
:::

:::{figure} ../assets/figures/phase-map-comparison.jpg
:alt: Ground-truth phase map of a simulated HZO film compared against phase maps recovered by two ACOM implementations
:width: 100%
Benchmarking phase mapping on simulated HZO data with known ground truth: recovered phase maps and reliability scores can be validated quantitatively before the method is trusted on experiments.
:::

## Practical notes

- Pattern matching is only as good as the calibration: the reciprocal pixel size can be refined by fitting the measured Bragg peak radial distribution against the structure factors of a known phase in the sample.
- Correlation score maps are worth inspecting on their own: low scores flag overlapping grains, unindexed phases, or regions where the library doesn't contain the right structure.
- Template matching of the *full patterns* (as in pyxem [](doi:10.1016/j.ultramic.2022.113517)) and sparse peak matching (as in py4DSTEM's ACOM) are complementary approaches; both are open source, so you can try each on your data.
- ACOM gives you strain for free: the distortion between each measured pattern and its best-matched simulation yields a per-phase strain map, with no manual choice of basis vectors.
