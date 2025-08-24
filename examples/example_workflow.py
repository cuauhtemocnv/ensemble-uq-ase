import numpy as np
from ase import Atoms
from ensemble_uq import EnsembleCalculator

# Dummy potential for demonstration
class DummyPotential:
    def __init__(self, energy_offset, force_offset):
        self.energy_offset = energy_offset
        self.force_offset = force_offset

    def get_potential_energy(self, atoms):
        return len(atoms) * 1.0 + self.energy_offset

    def get_forces(self, atoms):
        return np.random.normal(0, 0.1, (len(atoms), 3)) + self.force_offset

def main():
    # Create dummy calculators
    calculators = [
        DummyPotential(0.0, 0.01),
        DummyPotential(0.1, 0.02),
        DummyPotential(-0.1, -0.01),
        DummyPotential(0.2, 0.03),
        DummyPotential(-0.05, -0.02)
    ]

    # Ensemble calculator
    ensemble_calc = EnsembleCalculator(calculators, bias_strength=1.0)

    # H2O molecule
    atoms = Atoms("H2O", positions=[
        [0, 0, 0],
        [0.95, 0, 0],
        [0.95 * np.cos(np.radians(104.5)), 0.95 * np.sin(np.radians(104.5)), 0]
    ])
    atoms.calc = ensemble_calc

    print("Total Energy:", atoms.get_potential_energy())
    print("Forces:", atoms.get_forces())
    print("Stats:", ensemble_calc.get_ensemble_statistics())

if __name__ == "__main__":
    main()
