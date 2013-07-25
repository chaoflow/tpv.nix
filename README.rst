tpv.nix
=======

`tpv.nix` provides dictionary-like access to nix facilities for python
programmers.


Data model
----------

    hydra/
    store/


Hydra
~~~~~

Hydra_ is nix' continuous build farm. It provides a JSON API which we
facility to provide dictionary-like access for python programmers.

::

    >>> from tpv.nix.hydra import Hydra
    >>> hydra = Hydra()
    >>> hydra.keys()
    ['eval', 'jobset', 'project']

.. _Hydra: http://hydra.nixos.org


Nix store
~~~~~~~~~


    >>> from tpv.nix.store import Store
    >>> store = Store
    >>> store.keys()
    ['roots']


CLI
---

Install hello into the user's profile, in case of root the default
profile the two commands are equivalent::

    % xin install hello
    % xin install --profile profile hello

Install hello into the greetings profile, which resides in
$NIX_USER_PROFILE_DIR and needs to exist::

    % xin install --profile greetings hello

Remove a program::

    % xin remove --profile greetings hello

List installed programs::

    % xin list --profile greetings

Search programs::

    % xin search *ell*

List available profiles::

    % xin profile
    default
    greetings
    profile
    system

    % xin profile -v
    default   /nix/var/nix/profiles/default
    greetings /nix/var/nix/profiles/per-user/maakus/greetings
    profile   /nix/var/nix/profiles/per-user/maakus/profile
    system    /nix/var/nix/profiles/system

    % xin profile -v --porcelain
    default /nix/var/nix/profiles/default
    greetings /nix/var/nix/profiles/per-user/maakus/greetings
    profile /nix/var/nix/profiles/per-user/maakus/profile
    system /nix/var/nix/profiles/system

    % xin profile --output=json
    {
      "default": {"path": "/nix/var/nix/profiles/default"},
      "greetings": {"path": "/nix/var/nix/profiles/per-user/maakus/greetings"},
      "profile": {"path": "/nix/var/nix/profiles/per-user/maakus/profile"},
      "system": {"path": "/nix/var/nix/profiles/system"}
    }

Add a new profile in $NIX_USER_PROFILE_DIR::

    % xin profile add new_profile

XXX: nix-env currently needs at least one package to be added to the
profile in order to create it. Do we want to manage a separate list of
known profiles or create profiles implicitly?

Alternative::

    % xin install --profile greetings --create-profile hello

List generations of a profile::

    % xin profile list-generations new_profile
    486   2013-07-18 15:26:32   
    487   2013-07-23 12:22:22   
    488   2013-07-23 15:58:16   (current)

XXX: how do we select the profile?

Delete specific generations::

    % xin profile delete-generations 486 487
    % xin profile delete-generations <=487
    % xin profile delete-generations <488
    % xin profile delete-generations <2013-07-23
    % xin profile delete-generations "<2013-07-23 15:00"

XXX: how do we select the profile?

Or::

    % xin profile generations remove 486 487

XXX: how do we select the profile?

If you delete all generations the profile will be deleted as well::

    % xin profile generations remove --all new_profile


XXX: Maybe better::

Generations of user profile::

    % xin generations (-v)?
    486   2013-07-18 15:26:32   
    487   2013-07-23 12:22:22   
    488   2013-07-23 15:58:16   (current)

Generations of explicit profile::

    % xin generations --profile new_profile
    486   2013-07-18 15:26:32   
    487   2013-07-23 12:22:22   
    488   2013-07-23 15:58:16   (current)

::

    % xin generations remove 486 487
    % xin generations remove <=487
    % xin generations remove <488
    % xin generations remove <2013-07-23
    % xin generations remove "<2013-07-23 15:00"


Activate only a single profile, no default, no system::

    % xin profile activate new_profile (only this profile in path)


Activating a list of profiles::

    % xin profile activate 

    % xin update


Development
------------

    % xin devenv --python create 


Hydra
-----

    % xin hydra jobsets

    % xin hydra evaluation diff 456 500
