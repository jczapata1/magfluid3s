<h1 align="center">MagFluid3S</h1>

<div align="center">

![Version](https://img.shields.io/badge/Version-1.4.0-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg?logo=python&logoColor=white)
![Fortran](https://img.shields.io/badge/Fortran-any-red.svg)
![OpenMP](https://img.shields.io/badge/OpenMP-any-F7931E.svg)

</div>

<p align="justify">
<b>MagFluid3S</b> (Magnetic FluidS Stochastic Simulations) is a free and open-source software developed for the simulation of dynamic and thermodynamic properties of three-dimensional magnetic nanoparticle systems in a viscous medium. The framework allows users to model, initialize, execute, and post-process different types of simulations, including Microstates (observation of the dynamics of magnetic moment and easy-axis), MvsH (magnetization versus magnetic field, hysteresis loops), and MvsT (magnetization versus temperature, ZFC and FC protocols). The code supports flexible configuration of particle size distributions, material parameters, and initial magnetic states, enabling detailed studies of the magnetic response of nanoparticle ensembles under a wide range of experimental conditions.
</p>

<p align="justify">
Implemented in both Python and Fortran, the framework combines the versatility of Python for workflow control and data processing with the computational efficiency of Fortran–OpenMP for the numerical solvers. This hybrid design ensures both performance and usability. Particular emphasis is placed on reproducibility and extensibility, allowing users to modify, expand, and automate simulations to address new research challenges, especially in the fields of nanomagnetism and magnetic fluids.
</p>

Visit [MagFluid3S-Data](https://github.com/jczapata1/magfluid3s-data). 

## Documentation

Find the full documentation in the [User Guide v1.4.0](./User_Guide_v1.4.0.pdf).

## Installation

### 1. Install Docker

Download and install [Docker Desktop](https://www.docker.com/get-started).

### 2. Launch App

Open a terminal (PowerShell on Windows, or a terminal on Linux/macOS) and run:

```bash
docker run -it --name mf3s -p 127.0.0.1:8888:8888 jczapata1/magfluid3s:v1.4.0
```

To reopen the app later, run:

```bash
docker start -ai mf3s
```

### 3. Open Jupyter Notebook

Click the link ([http://127.0.0.1:8888/](http://127.0.0.1:8888/)) to open Jupyter Notebook in your browser.

### 4. Start a Simulation

Open and run the notebook [run.ipynb](./MagFluid3S/run.ipynb).

## Citation

If you use the **MagFluid3S** framework in your research, please cite:

> Zapata, J. C. and Restrepo, J. [*AIP Advances* **13**, 105110 (2023)](https://doi.org/10.1063/5.0164259).  

BibTeX:
```bibtex
@article{Zapata2023,
  author = {Zapata, J. C. and Restrepo, J.},
  title = {Dynamic hysteretic properties and specific loss power of magnetic nanoparticles in a viscous medium at different thermal baths},
  journal = {AIP Advances},
  volume = {13},
  pages = {105110},
  year = {2023},
  doi = {10.1063/5.0164259},
  url = {https://doi.org/10.1063/5.0164259}
}
```

## Copyright and License

Copyright © 2025-2026 J. C. Zapata. All rights reserved.

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.