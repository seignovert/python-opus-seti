===============================
OPUS
===============================
|Build| |Coverage| |PyPI| |Status| |Version| |Python| |License|

.. |Build| image:: https://travis-ci.org/seignovert/python-opus-seti.svg?branch=master
        :target: https://travis-ci.org/seignovert/python-opus-seti
.. |Coverage| image:: https://coveralls.io/repos/github/seignovert/python-opus-seti/badge.svg?branch=master
        :target: https://coveralls.io/github/seignovert/python-opus-seti?branch=master
.. |PyPI| image:: https://img.shields.io/badge/PyPI-opus-seti-blue.svg
        :target: https://pypi.python.org/project/opus-seti
.. |Status| image:: https://img.shields.io/pypi/status/opus-seti.svg?label=Status
.. |Version| image:: https://img.shields.io/pypi/v/opus-seti.svg?label=Version
.. |Python| image:: https://img.shields.io/pypi/pyversions/opus-seti.svg?label=Python
.. |License| image:: https://img.shields.io/pypi/l/opus-seti.svg?label=License

*Python package for OPUS_ (NASA-PDS/Seti) search tool API*

.. _OPUS: https://https://tools.pds-rings.seti.org/opus

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

.. code:: python

    >>> from opus import api

    >>> api.data(planet='Saturn', target='pan')

Note
----
**IMPORTANT:** I have no current affiliation with NASA or SETI. The package is provided "as is", use at your own risk.