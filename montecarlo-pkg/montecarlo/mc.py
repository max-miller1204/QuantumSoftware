"""Metropolis Monte Carlo sampling for Ising models."""

import numpy as np
import random

from .bitstring import BitString
from .ising import IsingHamiltonian


class MonteCarlo:
    """Metropolis Monte Carlo sampler for an Ising Hamiltonian.

    Parameters
    ----------
    ham : IsingHamiltonian
        The Hamiltonian to sample
    """

    def __init__(self, ham: IsingHamiltonian):
        self.ham = ham
        self.N = ham.N

    def run(self, T: float, n_samples: int = 1000, n_burn: int = 100):
        """Run Metropolis Monte Carlo sampling.

        For each MC step, sweep over all sites proposing single spin flips.
        Accept or reject based on the Metropolis criterion:
          - If dE <= 0: accept
          - If dE > 0: accept with probability exp(-dE/T)

        Parameters
        ----------
        T : float
            Temperature
        n_samples : int
            Number of samples to collect after burn-in
        n_burn : int
            Number of burn-in sweeps to discard

        Returns
        -------
        tuple of (energies, magnetizations)
            energies : np.ndarray of length n_samples
            magnetizations : np.ndarray of length n_samples
        """
        conf = BitString(self.N)
        # Start from a random configuration
        for i in range(self.N):
            if random.random() < 0.5:
                conf.flip_site(i)

        current_e = self.ham.energy(conf)

        energies = np.zeros(n_samples)
        magnetizations = np.zeros(n_samples)

        total_sweeps = n_burn + n_samples

        sites = list(range(self.N))
        sample_idx = 0
        for sweep in range(total_sweeps):
            # Sweep over all sites in random order
            random.shuffle(sites)
            for site in sites:
                # Propose a flip
                conf.flip_site(site)
                new_e = self.ham.energy(conf)
                dE = new_e - current_e

                if dE <= 0:
                    # Accept
                    current_e = new_e
                elif random.random() < np.exp(-dE / T):
                    # Accept with Boltzmann probability
                    current_e = new_e
                else:
                    # Reject: flip back
                    conf.flip_site(site)

            # Record after burn-in
            if sweep >= n_burn:
                energies[sample_idx] = current_e
                magnetizations[sample_idx] = conf.on() - conf.off()
                sample_idx += 1

        return energies, magnetizations
