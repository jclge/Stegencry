Installation
============

Notes
-----

.. note:: Stegencry is supported on the following Python versions

+----------------------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
|**Python**            |**3.8**|**3.7**|**3.6**|**3.5**|**3.4**|**3.3**|**3.2**|**2.7**|**2.6**|**2.5**|**2.4**|
+----------------------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
|Stegencry    **0.1.0**|  Yes  |  Yes  |  Yes  |  Yes  |  Yes  |       |       |       |       |       |       |
+----------------------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+

Warnings
--------

.. warning:: Stegencry and its creators can not be held responsible of any inconvenience. Include it in your projects at your own risk.

.. warning:: Please read properly the license.

Basic Installation
------------------

We provide a classic installation for most of Unix based distributions, we did not test it with Windows therefor we'll not support it yet::

    pip3 install stegencry

External Libraries
------------------

Stegencry requires external libraries. All bellow are required, for now.

* **PIL** provides image manipulation.

  * Stegencry has been tested with Pillow version **8.0.1**.

* **cryptography** provides the encryption key generation.

  * Stegencry has been tested with cryptography version **3.2.1**.

* **numpy** provides tools for the image generation.

  * Stegencry has been tester with numpy version **1.19.4**


External Dependencies
---------------------

.. note:: For now, there is no external dependency required.