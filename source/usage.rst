Overview
========

Notes
-----

.. note:: This project has been tested on a computer on Arch Linux and MacOS ; some features may not be compatible with non-Unix OS' or different kernels.

Warnings
--------

.. warning:: Stegencry cannot be held responsible for any harm the library could cause to your files. Please backup any image beforehand.

Function Prototypes
-------------------

Functions commun to the encrypt and decrypt Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**set_master**:
    .. note:: set_master is used to set the image that will be encrypted.
    .. warning:: This function is mandatory.
    *set_master(self, string)*

    set_master(self, [path_to_an_image])

    **Return value**: None

**set_slave**:
    .. note:: set_slave is used to set the image the master one will be hidden into with the function steganography
    .. warning:: This function is optionnal. It will generate an image on steganography call if not set.
    *set_slave(self, string)*

    set_slave(self, [path_to_an_image])

    **Return value**: None

**set_output**:
    .. note:: set_output sets the name of the output image. It can be the name of the master or of the slave.
    .. warning:: This function is mandatory.
    *set_output(self, string)*

    set_output(self, [path_to_an_image])

    **Return value**: None

**set_key**:
    .. note:: set_key sets the key to be used for the encryption / decrytion.
    .. warning:: This function is optionnal. If not used you have to generate a key.
    .. warning:: Only Stegencry generated keys are valid.
    *set_key(self, string)*

    set_key(self, [key])

    **Return value**: None

**print_key**:
    .. note:: print_key prints the current key, generated or given.
    .. warning:: This function is optionnal.
    *print_key(self)*

    print_key(self)

    **Return value**: None

**generate_key**:
    .. note:: generate_key generates a new key.
    .. warning:: This function is optionnal. If not used, you have to give a key yourself.
    *generate_key(self)*

    generate_key(self)

    **Return value**: None

**save_image**:
    .. note:: save_image saves the image at any point of the encryption
    .. warning:: This function is optionnal.
    *save_image(self)*

    save_image(self)

    **Return value**: None


Functions of the encrypt module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**steganography**:
    .. note:: steganography hides the master image into a slave image.
    .. warning:: This function cannot be used with encrypt_rgb but no error will be thrown (the image will be partially corrupted but still readable).
    .. warning:: This function automatically saves the image on the output the user has set.
    *steganography(self)*

    steganography(self)

    **Return value**: None

**shuffle_pixels**:
    .. note:: shuffle_pixels shuffles the pixels.
    .. warning:: This function is optionnal but makes a huge part of the encryption.
    *shuffle_pixels(self)*

    shuffle_pixels(self)

    **Return value**: None

**encrypt_rgb**:
    .. note:: encrypt_rgb encrypt the rgb values of each pixel.
    .. warning:: This function is optionnal and it is not recommended to use it with steganography.
    *encrypt_rgb(self)*

    encrypt_rgb(self)

    **Return value**: None

Functions of the decrypt module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**steganography**:
    .. note:: retrives an image hidden into another.
    .. warning:: This function automatically saves the image on the output the user has set.
    *steganography(self)*

    steganography(self)

    **Return value**: None

**unshuffle_pixels**:
    .. note:: unshuffle_pixels unshuffles the pixels.
    *unshuffle_pixels(self)*

    unshuffle_pixels(self)

    **Return value**: None

**decrypt_rgb**:
    .. note:: decrypt_rgb decrypt the rgb values of each pixel.
    *decrypt_rgb(self)*

    decrypt_rgb(self)

    **Return value**: None


Use Stegencry in your programs
---------------------------------

Import
^^^^^^

To properly use Stegencry in your projects, you only need to import it the following way::

    import Stegencry
    create_class_object = Stegencry.encrypt()
    create_class_object.set_master("path_to_file")

You also can import each method separately::

    from Stegencry import encrypt
    object = encrypt().set_master("path_to_file")

.. note:: All of the above examples do the same thing.