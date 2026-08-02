---
title: The open-source 4D-STEM software ecosystem
short_title: Software ecosystem
---

:::{admonition} Learning goals
:class: tip
- Know what py4DSTEM, quantEM, pyxem/HyperSpy, Kelvin_STEM, and abTEM each do best.
- Pick a sensible starting tool for a given analysis task.
:::

A healthy ecosystem of open-source Python packages has grown up around 4D-STEM analysis. They overlap in places, and that is a feature: you can move data between them, cross-check results, and pick the tool whose workflow fits your problem. This module gives a whirlwind tour of the packages used in this course.

## py4DSTEM

[py4DSTEM](https://github.com/py4dstem/py4DSTEM) [](doi:10.1017/S1431927621000477) is an open-source Python package for 4D-STEM analysis, developed at Lawrence Berkeley National Laboratory and by a broad community of contributors. It covers the full pipeline used in this course: file I/O across many vendor formats, calibration, virtual imaging, Bragg disk detection, strain mapping, automated crystal orientation mapping (ACOM), fluctuation microscopy, and phase contrast imaging methods including ptychography. Most of the hands-on Colab sessions today use py4DSTEM.

## quantEM

[quantEM](https://electronmicroscopy.github.io/quantem-docs/) is a newer open-source toolkit for quantitative electron microscopy built on PyTorch, so the same analysis code runs on CPUs and GPUs and integrates naturally with deep learning workflows. It spans imaging, diffraction, ptychography, tomography, and spectroscopy, and is under active development by several of the course instructors and collaborators ([code on GitHub](https://github.com/electronmicroscopy/quantem)).

## pyxem / HyperSpy

[pyxem](https://pyxem.readthedocs.io/) is a 4D-STEM analysis library built on the [HyperSpy](https://hyperspy.org/) multi-dimensional data framework. It is particularly strong for scanning (precession) electron diffraction workflows: template-matching orientation mapping [](doi:10.1016/j.ultramic.2022.113517), virtual imaging, and vector-based diffraction analysis, with lazy/out-of-core processing for datasets larger than memory via Dask.

## Kelvin_STEM

[Kelvin_STEM](https://github.com/maclariz/Kelvin_STEM) is a set of fast 4D-STEM analysis tools developed by Ian MacLaren's group at the University of Glasgow, used in this course for virtual imaging, digital dark field, and clustering workflows on large datasets.

## abTEM

[abTEM](https://abtem.readthedocs.io/) [](doi:10.12688/openreseurope.13015.1) simulates TEM and STEM experiments from first principles: multislice and PRISM image simulation directly from atomic models, entirely in Python. Simulation matters for 4D-STEM analysis: it lets you generate test data with known ground truth, design experiments (convergence angle, thickness, tilt sensitivity), and build the diffraction template libraries used in orientation mapping.

## Which tool should I use?

| Task | Good starting points |
| --- | --- |
| Load / browse / calibrate 4D data | py4DSTEM, pyxem, quantEM |
| Virtual imaging (BF/ADF/custom masks) | any of the above; Kelvin_STEM for speed on large data |
| Strain mapping | py4DSTEM, pyxem, quantEM |
| Orientation / phase mapping | py4DSTEM (ACOM), pyxem (template matching) |
| ML clustering / decomposition | pyxem + scikit-learn, Kelvin_STEM |
| Amorphous / PDF analysis | py4DSTEM, quantEM |
| Simulation | abTEM |
| Ptychography / phase retrieval | py4DSTEM, quantEM, abTEM (simulation) |
