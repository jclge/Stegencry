Tutorial & Examples
===================

encryption Module
-----------------

Steganography - Basic usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set the data to use the stenganography function::

    from Stegencry import encrypt
    obj = encrypt()
    obj.set_master("path_to_image")
    obj.set_slave("path_to_image")
    obj.set_output("path_to_output")
    obj.generate_key()

Call steganography and save the output::

    obj.steganography()

Steganography - Advanced Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: On this example we'll generate an image, encrypt the pixels and save the output.

Complete example::

    from Stegencry import encrypt
    obj = encrypt()
    obj.set_master("path_to_image")
    obj.set_output("path_to_output")
    obj.generate_key()
    obj.print_key()
    obj.shuffle_pixels()
    obj.steganography()


Shuffle_pixels - Basic usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set the data to use the shuffle_pixels function::

    from Stegencry import encrypt
    obj = encrypt()
    obj.set_master("path_to_image")
    obj.set_output("path_to_output")
    obj.generate_key()

Call shuffle_pixels and save the output::

    obj.shuffle_pixels()
    obj.save_image()

Shuffle_pixels - Advanced Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: On this example we'll encrypt the master image and its rgb values but we wont hide it in another one (see Steganography)

Complete example::

    from Stegencry import encrypt
    obj = encrypt()
    obj.set_master("path_to_image")
    obj.set_output("path_to_output")
    obj.generate_key()
    obj.print_key()
    obj.encrypt_rgb()
    obj.shuffle_pixels()
    obj.save_image()

Encrypt_rgb - Basic usage
^^^^^^^^^^^^^^^^^^^^^^^^^

Set the data to use the encrypt_rgb function::

    from Stegencry import encrypt
    obj = encrypt()
    obj.set_master("path_to_image")
    obj.set_output("path_to_output")
    obj.generate_key()

Call encrypt_rgb and save the output::

    obj.encrypt_rgb()
    obj.save_image()

Encrypt_rgb - Advanced Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: On this example we'll encrypt the master image and its rgb values but we wont hide it in another one (see Steganography)

Complete example::

    from Stegencry import encrypt
    obj = encrypt()
    obj.set_master("path_to_image")
    obj.set_output("path_to_output")
    obj.generate_key()
    obj.print_key()
    obj.encrypt_rgb()
    obj.shuffle_pixels()
    obj.save_image()

decryption Module
-----------------

Steganography - Basic usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set the data to use the stenganography function::

    from Stegencry import decrypt
    obj = decrypt()
    obj.set_master("path_to_image")
    obj.set_output("path_to_output")
    obj.set_key("key")

Call steganography and save the output::

    obj.steganography()

Steganography - Advanced Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: Here we'll retrive the image

Complete example::

    from Stegencry import decrypt
    obj = decrypt()
    obj.set_master("path_to_image")
    obj.set_output("path_to_output")
    obj.set_key("key")
    obj.steganography()
    obj.set_master("path_to_output")
    obj.unshuffle_pixels()
    obj.save_image()


Unshuffle_pixels - Basic usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set the data to use the unshuffle_pixels function::

    from Stegencry import decrypt
    obj = decrypt()
    obj.set_master("path_to_image")
    obj.set_output("path_to_output")
    obj.set_key("key")

Call unshuffle_pixels and save the output::

    obj.unshuffle_pixels()
    obj.save_image()

Unshuffle_pixels - Advanced Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: Here we'll retrive the image

Complete example::

    from Stegencry import decrypt
    obj = decrypt()
    obj.set_master("path_to_image")
    obj.set_output("path_to_output")
    obj.set_key("key")
    obj.unshuffle_pixels()
    obj.decrypt_rgb()
    obj.save_image()

Decrypt_rgb - Basic usage
^^^^^^^^^^^^^^^^^^^^^^^^^

Set the data to use the encrypt_rgb function::

    from Stegencry import decrypt
    obj = decrypt()
    obj.set_master("path_to_image")
    obj.set_output("path_to_output")
    obj.set_key("key")

Call encrypt_rgb and save the output::

    obj.decrypt_rgb()
    obj.save_image()

Encrypt_rgb - Advanced Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: Here we retrive the image

Complete example::

    from Stegencry import decrypt
    obj = decrypt()
    obj.set_master("path_to_image")
    obj.set_output("path_to_output")
    obj.set_key("key")
    obj.unshuffle_pixels()
    obj.decrypt_rgb()
    obj.save_image()