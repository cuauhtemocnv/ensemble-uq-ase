# Ensemble-UQ-ASE 🚀 for Active Learning
Uncertainty quantification for **interatomic potentials** using ensemble methods, built on top of [ASE (Atomic Simulation Environment)](https://wiki.fysik.dtu.dk/ase/).

This repository corresponds to part of the work presented in:

> **Beam induced heating in electron microscopy modeled with machine learning interatomic potentials**  
> Valencia, C. N., Lomholdt, W. B., Larsen, M. H. L., Hansen, T. W., & Schiøtz, J. (2024).  
> *Nanoscale, 16(11), 5750–5759.*  
> [https://doi.org/10.1039/D3NR05220F](https://doi.org/10.1039/D3NR05220F)

---
## ⚙️ How It Works

The `EnsembleCalculator` works as a drop-in ASE calculator that wraps multiple interatomic potentials (an **ensemble**).

- **Energy Calculation** (`atoms.get_potential_energy()`):
  Returns the mean energy of the ensemble, corrected with a bias term proportional to the energy variance:

  $$E_{\text{total}} = w*\bar{E} - r \cdot \sigma_E^2/N$$
  
  where:
  - $\bar{E}$ = mean energy across the ensemble
  - $\sigma_E^2$ = variance of the energies  
  - $r$ = bias strength parameter (user-defined)
  - $N$ = Number of atoms 

- **Force Calculation** (`atoms.get_forces()`):
  Returns the mean forces plus an additional bias force that points in the direction where the uncertainty is maximized:
```math
  \mathbf{F}_{\mathrm{bias}} = -r \sum_i (E_i - \bar{E}) (\mathbf{F}_i - \bar{\mathbf{F}})
```
```math
\mathbf{F}_{\mathrm{total}} = w*\bar{\mathbf{F}} + \mathbf{F}_{\mathrm{bias}}
```

  where:
  - $E_i$ = energy predicted by potential $i$
  - $\mathbf{F}_i$ = forces predicted by potential $i$
  - $\bar{E}$ = mean energy
  - $\bar{\mathbf{F}}$ = mean force
  - $w$ = weight for potential energy contribution, default=0

👉 This means the forces naturally push the atoms towards regions where the ensemble disagrees most, i.e., where the uncertainty is maximized.
---
## ✨ Features
- Drop-in replacement for any ASE `Calculator`.
- Works with **multiple ML/DFT potentials**.
- Provides both **total energy/forces** and **ensemble statistics**.
- Examples for quick start and reproducibility.

---

## 📦 Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/cuauhtemocnv/ensemble-uq-ase.git
cd ensemble-uq-ase
pip install -e .
```
Or just pip install
```bash
pip install git+https://github.com/cuauhtemocnv/ensemble-uq-ase.git
```

## 🚀 Quick Start

```python
from ase import Atoms
from ase.calculators.calculator import Calculator, all_changes
import numpy as np
from ensemble_uq import EnsembleCalculator
class DummyCoulombCalculator(Calculator):
    implemented_properties = ['energy', 'forces']

    def __init__(self, alpha=1.0, **kwargs):
        super().__init__(**kwargs)
        self.alpha = alpha

    def get_potential_energy(self, atoms, force_consistent=True):
        self.atoms = atoms
        pos = atoms.get_positions()
        numbers = atoms.get_atomic_numbers()
        energy = 0.0
        for i in range(len(atoms)):
            for j in range(i+1, len(atoms)):
                r_vec = pos[i] - pos[j]
                r = np.linalg.norm(r_vec)
                energy += self.alpha * numbers[i] * numbers[j] / r
        return energy

    def get_forces(self, atoms):
        pos = atoms.get_positions()
        numbers = atoms.get_atomic_numbers()
        forces = np.zeros_like(pos)
        for i in range(len(atoms)):
            for j in range(i+1, len(atoms)):
                r_vec = pos[i] - pos[j]
                r = np.linalg.norm(r_vec)
                f = self.alpha * numbers[i] * numbers[j] * r_vec / r**3
                forces[i] += f
                forces[j] -= f
        return forces

# Example molecule
atoms = Atoms("H2O", positions=[
    [0.0, 0.0, 0.0],
    [0.95, 0.0, 0.0],
    [0.95, 0.95, 0.0]
])

# Set calculator with alpha scaling
atoms.calc = DummyCoulombCalculator(alpha=0.1)
# Create an ensemble of dummy calculators
calculators = [
    DummyCoulombCalculator(0.01),
    DummyCoulombCalculator(0.2),
    DummyCoulombCalculator(0.3)
]
ensemble_calc = EnsembleCalculator(calculators,w_means=0.0)

# Simple H2O molecule
atoms = Atoms("H2O", positions=[
    [0, 0, 0],
    [0.95, 0, 0],
    [0.95, 0.95, 0]
])
atoms.calc = ensemble_calc

print("Energy:", atoms.get_potential_energy
print("Forces:", atoms.get_forces())
print("Stats:", ensemble_calc.get_ensemble_statistics())
```
## 📂 Examples

This repository includes a couple of ready-to-run examples:

- [**example_workflow.py**](examples/example_workflow.py)  
  Full ASE workflow using the `EnsembleCalculator` on a water molecule (H₂O).  
  Demonstrates ensemble statistics, energies, and forces.

- [**simple_usage.py**](examples/simple_usage.py)  
  Minimal quick-start example showing how to initialize an ensemble with dummy calculators.

📜 Citation
If you use this repository in your research, please cite:
```bibtex
Beam induced heating in electron microscopy modeled with machine learning interatomic potentials
Valencia, C. N., Lomholdt, W. B., Larsen, M. H. L., Hansen, T. W., & Schiøtz, J. (2024).
Nanoscale, 16(11), 5750–5759.
https://doi.org/10.1039/D3NR05220F

bibtex
```
