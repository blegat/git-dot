.. -*- coding: utf-8 -*-

git-dot
=======

This utility generates a graph in the
`dot format <http://www.graphviz.org/doc/info/lang.html>`_
showing the `Git <http://git-scm.com>` history.

Install
-------

You can install it from source by cloning this repo

.. code-block:: bash

    git clone https://github.com/blegat/git-dot.git

and running

.. code-block:: bash

    sudo python setup.py install

You can also install the latest released version through ``pip``

.. code-block:: bash

    sudo pip install git-dot

or ``easy_install``

.. code-block:: bash

    sudo easy_install git-dot

Usage
-----

You can get help by running

.. code-block:: bash

    git-dot -h

You can get graph in a PNG format using
`Graphviz <http://www.graphviz.org/>`_ like this

.. code-block:: bash

    git-dot graph.dot
    dot -Tpng -o graph.png graph.dot
