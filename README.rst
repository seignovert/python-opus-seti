OPUS
===============================

|Build| |Coverage| |PyPI| |Status| |Version| |Python| |License| |DOI|

.. |Build| image:: https://travis-ci.org/seignovert/python-opus-seti.svg?branch=master
        :target: https://travis-ci.org/seignovert/python-opus-seti
.. |Coverage| image:: https://coveralls.io/repos/github/seignovert/python-opus-seti/badge.svg?branch=master
        :target: https://coveralls.io/github/seignovert/python-opus-seti?branch=master
.. |PyPI| image:: https://img.shields.io/badge/PyPI-opus--seti-blue.svg
        :target: https://pypi.org/project/opus-seti
.. |Status| image:: https://img.shields.io/pypi/status/opus-seti.svg?label=Status
        :target: https://pypi.org/project/opus-seti
.. |Version| image:: https://img.shields.io/pypi/v/opus-seti.svg?label=Version
        :target: https://pypi.org/project/opus-seti
.. |Python| image:: https://img.shields.io/pypi/pyversions/opus-seti.svg?label=Python
        :target: https://pypi.org/project/opus-seti
.. |License| image:: https://img.shields.io/pypi/l/opus-seti.svg?label=License
        :target: https://pypi.org/project/opus-seti
.. |DOI| image:: https://www.zenodo.org/badge/134827243.svg
        :target: https://www.zenodo.org/badge/latestdoi/134827243

Python package for OPUS-Seti_ API_ (`NASA-PDS Rings Node`_)

.. _OPUS-Seti: https://tools.pds-rings.seti.org/opus/
.. _API: https://tools.pds-rings.seti.org/opus/api/
.. _`NASA-PDS Rings Node`: https://pds-rings.seti.org/

Install
-------
With ``pip``:

.. code:: bash

    $ pip install opus-seti

With the ``source files``:

.. code:: bash

    $ git clone https://github.com/seignovert/python-opus-seti.git
    $ cd opus-seti ; python setup.py install

Usage
------

.. code:: bash

    opus -h # For help

    opus --planet Saturn --target pan

    cassini-vims TITAN --limit 5

.. code:: python

    >>> from opus import api

    >>> api.data(planet='Saturn', target='pan', limit=10)
    OPUS API Data objects (with 10 elements):
    - S_IMG_CO_ISS_1480614021_N
    - S_IMG_CO_ISS_1488190255_N
    - S_IMG_CO_ISS_1488273311_N
    - S_IMG_CO_ISS_1488368442_N
    - S_IMG_CO_ISS_1488485562_N
    - S_IMG_CO_ISS_1488551713_N
    - S_IMG_CO_ISS_1488711044_N
    - S_IMG_CO_ISS_1488745124_N
    - S_IMG_CO_ISS_1488812400_N
    - S_IMG_CO_ISS_1488826725_N

More examples are available in this
`Jupyter Notebook`_.

.. _`Jupyter Notebook`: https://nbviewer.jupyter.org/github/seignovert/python-opus-seti/blob/master/jupyter_notebooks/examples.ipynb

Note
----
**IMPORTANT:** I have no current affiliation with NASA or SETI. The package is provided *as is*, use at your own risk.