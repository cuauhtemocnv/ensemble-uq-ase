import numpy as np
from ase.calculators.calculator import Calculator, all_changes

class EnsembleCalculator(Calculator):
    """
    ASE Calculator that combines multiple interatomic potentials into an ensemble
    Provides unified interface for energy and force calculations.
    """

    implemented_properties = ['energy', 'forces']

    def __init__(self, calculators, bias_strength: float = 1.0, w_means: float=0.0, **kwargs):
        """
        Initialize ensemble calculator.

        Parameters
        ----------
        calculators : list
            List of ASE-compatible calculators (or dummy calculators for testing).
        bias_strength : float, optional
            Strength parameter 'r' for energy bias regularization.
        """
        Calculator.__init__(self, **kwargs)
        self.calculators = calculators
        self.M = len(calculators)
        self.bias_strength = bias_strength
        self.w_means = w_means
        self.results = {}

    def calculate(self, atoms=None, properties=['energy', 'forces'],
                 system_changes=all_changes):
        """Main calculation method called by ASE."""
        Calculator.calculate(self, atoms, properties, system_changes)

        energies, forces_list = self._get_predictions(atoms)

        mean_energy = np.mean(energies)
        mean_forces = np.mean(forces_list, axis=0)
        na=len(atoms)
        energy_variance = self._calculate_energy_variance(energies, mean_energy)
        energy_bias = self._calculate_energy_bias(energy_variance)/na

                     
        bias_forces = self._calculate_bias_forces(
            energies, forces_list, mean_energy, mean_forces
        )

        total_energy = self.w_means*mean_energy-energy_bias
        total_forces = self.w_means*mean_forces + bias_forces

        self.results = {
            'energy': total_energy,
            'forces': total_forces,
            'mean_energy': mean_energy,
            'energy_bias': energy_bias,
            'energy_variance': energy_variance,
            'mean_forces': mean_forces,
            'bias_forces': bias_forces,
            'individual_energies': energies,
            'individual_forces': forces_list
        }

    def _get_predictions(self, atoms):
        """Get energy and force predictions from all calculators."""
        energies = np.zeros(self.M)
        forces_list = []

        for i, calc in enumerate(self.calculators):
            atoms.calc = calc
            energies[i] = atoms.get_potential_energy()
            forces_list.append(atoms.get_forces().copy())

        return energies, forces_list

    def _calculate_energy_variance(self, energies, mean_energy):
        """Variance of energy predictions."""
        return np.mean((energies - mean_energy) ** 2)

    def _calculate_energy_bias(self, energy_variance):
        """Energy bias term E_bias = r * σ_E²."""
        return self.bias_strength * energy_variance

    def _calculate_bias_forces(self, energies, forces_list, mean_energy, mean_forces):
        """Bias forces using derivative relationship."""
        n_atoms, n_dim = forces_list[0].shape
        bias_forces = np.zeros((n_atoms, n_dim))

        for i in range(self.M):
            energy_diff = energies[i] - mean_energy
            force_diff = forces_list[i] - mean_forces
            bias_forces += energy_diff * force_diff

        return -self.bias_strength * bias_forces

    def get_ensemble_statistics(self):
        """Return ensemble statistics dictionary."""
        if not self.results:
            return {}

        return {
            'mean_energy': self.results.get('mean_energy', 0.0),
            'energy_bias': self.results.get('energy_bias', 0.0),
            'energy_variance': self.results.get('energy_variance', 0.0),
            'total_energy': self.results.get('energy', 0.0),
            'n_potentials': self.M,
            'bias_strength': self.bias_strength,
            'individual_energies': self.results.get('individual_energies', []),
            'individual_forces': self.results.get('individual_forces', [])
        }
