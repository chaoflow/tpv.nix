tpv.nix
=======

`tpv.nix` provides dictionary-like access to nix facilities for python
programmers.

Hydra
-----

Hydra_ is nix' continuous build farm. It provides a JSON API which we
facility to provide dictionary-like access to its data for python
programmers.

    >>> from tpv.nix.hydra import Hydra
    >>> hydra = Hydra()
    >>> hydra.keys()
    ['eval', 'jobset', 'project']

.. _Hydra: http://hydra.nixos.org


Nix store
---------

