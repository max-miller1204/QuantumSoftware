Developer Guide
===============

Contributions are welcome.

Setting up a development environment
------------------------------------

Clone the repository and install in editable mode together with the test
dependencies:

.. code-block:: sh

    git clone https://github.com/max-miller1204/montecarlo.git
    cd montecarlo
    pip install -e ".[test]"

Running the tests
-----------------

The test suite is run with `pytest`_:

.. code-block:: sh

    pytest

.. _pytest: https://docs.pytest.org/

Building the documentation
--------------------------

Documentation is built with `Sphinx`_. From the ``docs/`` directory:

.. code-block:: sh

    make html

The generated HTML lives in ``docs/_build/html``.

.. _Sphinx: https://www.sphinx-doc.org/

Submitting changes
------------------

1. Fork the repository on GitHub.
2. Create a feature branch.
3. Make your changes, ensuring tests pass and new behaviour is covered by
   tests and docstrings.
4. Open a pull request describing the change.
