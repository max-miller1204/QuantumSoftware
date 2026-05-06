User Guide
==========

This guide covers the physics implemented by ``montecarlo`` and how to apply
it to your own graphs.

The Ising model
---------------

For a graph :math:`G = (V, E)` with edge weights :math:`J_{ij}`, ``montecarlo``
represents an Ising model with Hamiltonian

.. math::

    H(\alpha) = \sum_{(i,j) \in E} J_{ij}\, s_i s_j + \sum_{i \in V} \mu_i s_i,

where :math:`s_i = +1` if site :math:`i` is "up" (bit value 1) and
:math:`s_i = -1` if it is "down" (bit value 0). Each configuration
:math:`\alpha` is represented by a :class:`~montecarlo.BitString`.

Representing configurations
---------------------------

The :class:`~montecarlo.BitString` class wraps a NumPy array of 0/1 entries
and exposes utilities for flipping bits, counting up/down spins, and
converting to and from a decimal integer index:

.. code-block:: python

    import montecarlo

    bs = montecarlo.BitString(N=4)
    bs.set_integer_config(11)   # binary 1011
    print(bs)                   # "1011"
    print(bs.on(), bs.off())    # 3, 1
    bs.flip_site(0)             # now "0011"

Building a Hamiltonian
----------------------

Hamiltonians are constructed from a NetworkX graph with ``weight`` attributes
on each edge. Optional local fields can be set with ``set_mu``:

.. code-block:: python

    import networkx as nx
    import montecarlo

    N = 6
    G = nx.Graph()
    G.add_nodes_from(range(N))
    G.add_edges_from([(i, (i + 1) % N) for i in range(N)])
    for e in G.edges:
        G.edges[e]['weight'] = 2.0

    ham = montecarlo.IsingHamiltonian(G)
    ham.set_mu([0.1] * N)

    bs = montecarlo.BitString(N)
    bs.set_config([1, 0, 1, 0, 1, 0])
    print(ham.energy(bs))

Exact thermodynamic averages
----------------------------

Given the Boltzmann distribution

.. math::

    P(\alpha) = \frac{e^{-\beta E(\alpha)}}{Z}, \qquad
    Z = \sum_{\alpha'} e^{-\beta E(\alpha')},

an expectation value of an observable :math:`A` is

.. math::

    \langle A \rangle = \sum_\alpha A(\alpha) P(\alpha).

The :meth:`~montecarlo.IsingHamiltonian.compute_average_values` method
enumerates all :math:`2^N` configurations and returns

.. math::

    \langle E \rangle, \quad
    \langle M \rangle, \quad
    \frac{\langle E^2 \rangle - \langle E \rangle^2}{T^2}, \quad
    \frac{\langle M^2 \rangle - \langle M \rangle^2}{T},

i.e. the average energy, magnetization, heat capacity, and magnetic
susceptibility:

.. code-block:: python

    E, M, HC, MS = ham.compute_average_values(T=1.0)

This is exact, but its cost grows as :math:`2^N` and becomes infeasible
beyond roughly 20 sites.

Metropolis sampling
-------------------

For larger systems, :class:`~montecarlo.MonteCarlo` performs Metropolis
sampling. From the current configuration :math:`\alpha`, a single-site flip
proposes a new configuration :math:`\beta`, accepted with probability

.. math::

    W(\alpha \to \beta) =
    \begin{cases}
        1 & \text{if } E(\beta) \le E(\alpha) \\
        e^{-\beta\, [E(\beta) - E(\alpha)]} & \text{otherwise.}
    \end{cases}

The resulting Markov chain converges to the Boltzmann distribution, so
expectation values reduce to a simple arithmetic average over collected
samples:

.. math::

    \langle A \rangle \approx \frac{1}{M} \sum_{\alpha \in \text{trajectory}} A(\alpha).

.. code-block:: python

    import numpy as np

    mc = montecarlo.MonteCarlo(ham)
    E_samples, M_samples = mc.run(T=2.0, n_samples=10_000, n_burn=200)

    Eavg, Estd = np.mean(E_samples), np.std(E_samples)
    Mavg, Mstd = np.mean(M_samples), np.std(M_samples)

    HC = Estd**2 / 2.0**2
    MS = Mstd**2 / 2.0

The ``n_burn`` argument discards an initial number of sweeps to allow the
chain to equilibrate before recording samples. Each "sweep" attempts a flip
on every site once.

Temperature scans
-----------------

A common workflow is to compute observables across a range of temperatures
and locate the critical temperature, where the heat capacity and magnetic
susceptibility peak:

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt

    Ts = np.linspace(0.1, 10.0, 100)
    Es, Ms, HCs, MSs = [], [], [], []
    for T in Ts:
        E, M, HC, MS = ham.compute_average_values(T)
        Es.append(E); Ms.append(M); HCs.append(HC); MSs.append(MS)

    plt.plot(Ts, Es, label="Energy")
    plt.plot(Ts, Ms, label="Magnetization")
    plt.plot(Ts, HCs, label="Heat capacity")
    plt.plot(Ts, MSs, label="Susceptibility")
    plt.xlabel("Temperature"); plt.legend(); plt.show()

    Tc = Ts[int(np.argmax(MSs))]
    print(f"Critical temperature ~ {Tc:.2f}")
