# Ensemble-UQ-ASE 🚀
Uncertainty quantification for **interatomic potentials** using ensemble methods, built on top of [ASE (Atomic Simulation Environment)](https://wiki.fysik.dtu.dk/ase/).

This repository corresponds to part of the work presented in:

> **Beam induced heating in electron microscopy modeled with machine learning interatomic potentials**  
> Valencia, C. N., Lomholdt, W. B., Larsen, M. H. L., Hansen, T. W., & Schiøtz, J. (2024).  
> *Nanoscale, 16(11), 5750–5759.*  
> [https://doi.org/10.1039/D3NR05220F](https://doi.org/10.1039/D3NR05220F)

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
git clone https://github.com/your-username/ensemble-uq-ase.git
cd ensemble-uq-ase
pip install -e .
```
## 🚀 Quick Start

```python
from ase import Atoms
from ensemble_uq import EnsembleCalculator

# Define your calculators (replace DummyPotentials with actual ML/DFT calculators)
class DummyPotential:
    def __init__(self, energy_offset, force_offset):
        self.energy_offset = energy_offset
        self.force_offset = force_offset

    def get_potential_energy(self, atoms):
        return len(atoms) * 1.0 + self.energy_offset

    def get_forces(self, atoms):
        import numpy as np
        return np.random.normal(0, 0.1, (len(atoms), 3)) + self.force_offset

# Create an ensemble of dummy calculators
calculators = [
    DummyPotential(0.0, 0.01),
    DummyPotential(0.1, 0.02),
    DummyPotential(-0.1, -0.01)
]
ensemble_calc = EnsembleCalculator(calculators)

# Simple H2O molecule
atoms = Atoms("H2O", positions=[
    [0, 0, 0],
    [0.95, 0, 0],
    [0.95, 0.95, 0]
])
atoms.calc = ensemble_calc

print("Energy:", atoms.get_potential_energy())
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
