import numpy as np
from ase import Atoms
from ensemble_uq import EnsembleCalculator

class DummyPotential:
    def __init__(self, energy_offset, force_offset):
        self.energy_offset = energy_offset
        self.force_offset = force_offset

    def get_potential_energy(self, atoms):
        return len(atoms) * 1.0 + self.energy_offset

    def get_forces(self, atoms):
        return np.ones((len(atoms), 3)) * self.force_offset

def test_energy_and_forces():
    calculators = [
        DummyPotential(0.0, 0.0),
        DummyPotential(0.1, 0.1),
        DummyPotential(-0.1, -0.1),
    ]
    ensemble = EnsembleCalculator(calculators, bias_strength=1.0)

    atoms = Atoms("H2", positions=[[0,0,0],[0.7,0,0]])
    atoms.calc = ensemble

    energy = atoms.get_potential_energy()
    forces = atoms.get_forces()

    stats = ensemble.get_ensemble_statistics()

    assert isinstance(energy, float)
    assert forces.shape == (2, 3)
    assert stats["n_potentials"] == 3
    assert stats["energy_variance"] >= 0
