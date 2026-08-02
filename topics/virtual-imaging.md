---
title: Virtual dark field and digital dark field imaging
short_title: Virtual & digital dark field
---

:::{admonition} Hands-on tutorial
:class: important
- ▶️ [Virtual dark field and digital dark field (BFBT ceramic)](https://drive.google.com/file/d/1SwcFZd6bZJytR38UXeSiqpVuTk6yJnbX/view?usp=sharing)
:::

:::{admonition} Learning goals
:class: tip
- Form virtual bright field, dark field, and custom-mask images from a 4D dataset.
- Use digital dark field imaging to map grains, domains, and superlattice ordering from individual reflections.
- Design virtual detector geometries deliberately rather than by habit.
:::

Because a 4D-STEM dataset contains the *entire* diffraction pattern at every probe position, any STEM detector geometry can be applied *after* the experiment: integrate the intensity inside a chosen region of the diffraction pattern at each probe position, and the result is an image. This is **virtual imaging**, and it is usually the first, and often the most informative, analysis applied to any 4D-STEM dataset. Virtual bright field and dark field reconstruction in this sense was popularized by Rauch and co-workers alongside scanning precession diffraction and ACOM [](doi:10.1111/jmi.12065), [](doi:10.1016/j.matchar.2014.08.010), and generalized to arbitrarily shaped virtual apertures by Gammer et al. [](doi:10.1016/j.ultramic.2015.03.015).

## Virtual bright field and dark field

A circular mask over the central beam gives a virtual bright field (BF) image; an annulus outside it gives a virtual annular dark field (ADF). The two are complementary: electrons scattered out of the BF disk land in the DF detector, so regions that darken in BF brighten in DF. Unlike physical detectors, virtual detectors are free: you can try any inner/outer radius, any shape, any position, and iterate until the contrast isolates the feature you care about [](doi:10.1017/S1431927620024307):

:::{figure} ../assets/figures/virtual-masks.png
:alt: Virtual detector geometries applied to a diffraction pattern: a single aperture, an annular aperture, and an array of apertures over the diffracted spots
:width: 95%
Virtual detectors are defined in software after the experiment: a single aperture over one reflection, an annulus, or an aperture array matched to a whole family of diffracted spots.
:::

- **Detector design matters.** The BF detector should capture the unscattered disk (slightly expanded to tolerate residual descan); the ADF annulus geometry controls whether contrast is dominated by diffraction (low angles) or thickness/Z (high angles).
- **Selected-area diffraction in reverse:** integrating diffraction patterns over a *real-space* region of interest gives a virtual selected-area pattern from exactly that region, ideal for identifying which reflections belong to which microstructural feature.

## Digital dark field

Classical dark field TEM tilts the beam (or shifts the objective aperture) so one chosen Bragg reflection forms the image:

:::{figure} ../assets/figures/df-tem-schematic.png
:alt: Ray diagram of dark field imaging in conventional TEM using an objective aperture in the back focal plane
:width: 60%
Conventional dark field TEM: an objective aperture in the back focal plane selects a single diffracted beam to form the image: one reflection, one exposure, one tilt condition at a time.
:::

The 4D-STEM equivalent, **digital dark field (DDF)** [](doi:10.1093/mam/ozae104), places a virtual aperture over one (or several) specific Bragg reflections and maps where in real space that reflection is excited. Every reflection in the dataset is available simultaneously, from a single scan:

:::{figure} ../assets/figures/ddf-workflow.jpg
:alt: Flowchart of the digital dark field workflow, from probe template and peak finding through single apertures, aperture arrays, or points-list reduction to virtual dark field images
:width: 75%
The DDF workflow: after peak finding and g-vector identification, images can be formed from a single virtual aperture, from a mask built on a whole array of aperture positions, or by reducing the detected points list directly against the aperture array.
:::

This is enormously powerful for microstructure:

- **Grain and domain mapping:** each grain lights up only in the reflections it produces, so DDF images segment grains, twins, and ferroelastic/ferroelectric domains, even when they are invisible in BF/ADF contrast [](doi:10.1017/S1431927620024411).
- **Superlattice and ordered phases:** placing the aperture on superlattice reflections maps ordered regions and antiphase domains directly:

:::{figure} ../assets/figures/ddf-superlattice.jpg
:alt: Digital dark field maps of a perovskite film formed from different superlattice and higher-order Laue zone reflections, each highlighting a different ordered region
:width: 100%
Digital dark field in action on a perovskite thin film: virtual apertures on different superlattice and higher-order Laue zone reflections (right) map chemically and structurally distinct ordered regions through the film (left), all from one 4D-STEM scan.
:::

- **Tracking spots, not just masking them:** in real datasets the reflections move (strain, rotation, descan), so robust DDF implementations follow the peak within a window rather than using a fixed mask; this is where Bragg-vector-based approaches and fast implementations ([Kelvin_STEM](https://github.com/maclariz/Kelvin_STEM), py4DSTEM, pyxem) come in.
- From the ensemble of DDF images, phase and domain maps of the whole field of view can be assembled, the manual counterpart of the [ML clustering approaches](./ml-clustering.md) in the next module.
