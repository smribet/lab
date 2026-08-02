---
title: Orientation and flowline mapping of semicrystalline polymers
short_title: Semicrystalline polymers
---

:::{admonition} Hands-on tutorial
:class: important
- ▶️ [Flowline mapping of a semicrystalline polymer](https://drive.google.com/file/d/17G99GpRyoZBK7xFpPUVF-2AHsrq8nsnq/view?usp=drive_link): from diffuse arcs to orientation histograms to flowline maps, working in polar coordinates.
:::

:::{admonition} Learning goals
:class: tip
- Design a 4D-STEM experiment within the dose budget of a beam-sensitive material.
- Extract crystallite orientation from azimuthal arc positions at each probe position.
- Render orientation fields as flowline maps and read connectivity, domains, and defects from them.
:::

Semicrystalline polymers and small-molecule organic films (conjugated polymers for organic electronics, polyolefins, peptide and protein assemblies) derive their properties from nanoscale crystalline domains embedded in an amorphous matrix. Charge transport in an organic semiconductor, for example, depends on how the π-stacking direction of crystallites connects across the film. These materials are essentially impossible to characterize by conventional high-resolution imaging: they are extremely beam sensitive, with critical fluences of order 1–100 e⁻/Å², destroyed long before an atomic-resolution image can be formed [](doi:10.1021/acs.accounts.1c00073).

Nanobeam 4D-STEM sidesteps this. Diffraction concentrates the structural information from the whole illuminated volume into a few sharp features, so a useful diffraction pattern can be recorded with orders of magnitude fewer electrons than an image [](doi:10.1016/j.micron.2016.05.008), and with a fast camera, the dose is spread over the full field of view in a single low-fluence pass.

## From diffraction patterns to orientation maps

Polymer crystallites typically produce a strong, characteristic reflection (e.g., the ~3.6 Å π–π stacking peak in P3HT, or lamellar/backbone reflections at lower angles). Because of local disorder, these appear as azimuthal *arcs* rather than sharp spots:

:::{figure} ../assets/figures/polymer-diffraction.png
:alt: A nanobeam diffraction pattern from a semicrystalline polymer showing azimuthal arcs
:width: 55%
A single nanobeam pattern from a semicrystalline polymer: the characteristic reflections appear as azimuthal arcs whose angular position encodes the local crystallite orientation.
:::

The workflow:

1. **Detect the arcs.** At each probe position, locate the azimuthal position of the characteristic reflection. Polar transformation of each pattern makes the azimuthal intensity distribution easy to fit, and peak *prominence* (rather than absolute intensity) is the robust detection criterion for weak, diffuse signal.
2. **Map orientation.** The azimuthal angle of the arc gives the local crystallite orientation (modulo the symmetry of the reflection); its intensity gives the degree of crystallinity/alignment. The result is an orientation field over the scanned area.
3. **Draw flowlines.** Orientation fields are hard to read as color maps alone. **Flowline maps** [](doi:10.1038/s41563-019-0387-3), streamlines integrated through the orientation vector field drawn with density proportional to local alignment, render the connectivity of the crystalline regions directly, in images reminiscent of van Gogh's *Starry Night*:

:::{figure} ../assets/figures/flowline-maps.jpg
:alt: Orientation color map and flowline rendering of crystalline domains in a semicrystalline polymer film
:width: 100%
From orientation field to flowlines: the same region shown as an orientation color map (left) and as a flowline map (right). Connectivity, domain size, and topological defects in the orientation field become immediately readable.
:::

## Dose-limited experiment design

Everything about these experiments is a dose budget negotiation:

- **Total fluence** must stay below the damage threshold; measure the critical dose for your material first (e.g., by watching a reflection fade under repeated exposure).
- **Step size vs. probe size:** large scan steps (often ≫ probe size) spread the dose; the orientation field is smooth enough that sparse sampling still captures it.
- **Cryo helps:** cooling typically increases critical dose by a factor of a few.
- **Detector:** electron counting and high frame rates let you work at the shot-noise limit; pattern-level denoising and radial-symmetry priors can be applied in analysis.
