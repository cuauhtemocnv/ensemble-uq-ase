# Ensemble-UQ-ASE 🚀
Uncertainty quantification for **interatomic potentials** using ensemble methods, built on top of [ASE (Atomic Simulation Environment)](https://wiki.fysik.dtu.dk/ase/).

This repo provides a custom ASE `Calculator` that:
- Combines multiple interatomic potentials into an **ensemble**.
- Computes mean energies and forces.
- Quantifies **uncertainty via variance** in energy predictions.
- Applies a **bias correction** to improve robustness.
- Outputs detailed statistics (individual energies, forces, variance, etc.).

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
