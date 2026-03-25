"""Ising Hamiltonian class for computing energies and thermodynamic averages."""

import numpy as np
import networkx as nx

from .bitstring import BitString


class IsingHamiltonian:
    """Ising Hamiltonian defined on a graph.

    H = sum_{(i,j) in E} J_ij s_i s_j + sum_i mu_i s_i

    where s_i = +1 if bit i is 1 (up) and s_i = -1 if bit i is 0 (down).
    """

    def __init__(self, G: nx.Graph):
        self.G = G
        self.N = G.number_of_nodes()
        self.mu = np.zeros(self.N)
        self.J = G

    def set_mu(self, mus):
        """Set the local magnetic field terms.

        Parameters
        ----------
        mus : array-like
            Magnetic field values for each site

        Returns
        -------
        self
            Returns self for chaining
        """
        self.mu = np.array(mus)
        return self

    def energy(self, config: BitString):
        """Compute the energy of a BitString configuration.

        Parameters
        ----------
        config : BitString
            Input spin configuration

        Returns
        -------
        float
            Energy of the configuration
        """
        spins = 2 * config.config - 1

        e = 0.0
        for (i, j) in self.G.edges():
            Jij = self.G.edges[i, j]['weight']
            e += Jij * spins[i] * spins[j]

        e += np.dot(self.mu, spins)

        return e

    def compute_average_values(self, T: float):
        """Compute exact thermodynamic averages at temperature T.

        Enumerates all 2^N configurations and computes Boltzmann-weighted
        averages of energy, magnetization, heat capacity, and magnetic
        susceptibility.

        Parameters
        ----------
        T : float
            Temperature

        Returns
        -------
        tuple of (E, M, HC, MS)
            E  : average energy
            M  : average magnetization
            HC : heat capacity
            MS : magnetic susceptibility
        """
        beta = 1.0 / T
        bs = BitString(self.N)

        n_configs = 2 ** self.N

        energies = np.zeros(n_configs)
        magnetizations = np.zeros(n_configs)

        for i in range(n_configs):
            bs.set_integer_config(i)
            energies[i] = self.energy(bs)
            magnetizations[i] = bs.on() - bs.off()

        # Shift energies for numerical stability
        e_min = np.min(energies)
        boltzmann = np.exp(-beta * (energies - e_min))
        Z = np.sum(boltzmann)
        probs = boltzmann / Z

        E = np.dot(probs, energies)
        E2 = np.dot(probs, energies ** 2)
        M = np.dot(probs, magnetizations)
        M2 = np.dot(probs, magnetizations ** 2)

        HC = (E2 - E ** 2) / (T ** 2)
        MS = (M2 - M ** 2) / T

        return E, M, HC, MS
