Getting Started
===============

This page walks through installing ``montecarlo`` and running a first
Ising-model calculation.

Installation
------------

``montecarlo`` requires Python 3.8 or higher and depends on NumPy and
NetworkX. Clone the repository and install it in development mode:

.. code-block:: sh

    git clone https://github.com/max-miller1204/montecarlo.git
    cd montecarlo
    pip install -e .

To also install the test dependencies, use:

.. code-block:: sh

    pip install -e ".[test]"

Quickstart
----------

The example below builds a 6-site ring with antiferromagnetic coupling and
computes exact thermodynamic averages at temperature ``T = 1``:

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
    E, M, HC, MS = ham.compute_average_values(T=1.0)

    print(f"E  = {E:.6f}")
    print(f"M  = {M:.6f}")
    print(f"HC = {HC:.6f}")
    print(f"MS = {MS:.6f}")

For systems where exact enumeration of all :math:`2^N` configurations is too
expensive, use the Metropolis sampler:

.. code-block:: python

    mc = montecarlo.MonteCarlo(ham)
    energies, magnetizations = mc.run(T=2.0, n_samples=10_000, n_burn=200)

    import numpy as np
    print(f"<E> ~ {np.mean(energies):.4f}")
    print(f"<M> ~ {np.mean(magnetizations):.4f}")

See the :doc:`user_guide` for a more detailed walkthrough and the
:doc:`api` for the full API reference.
