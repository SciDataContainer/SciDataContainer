Advanced usage
==============

Convenience Methods
-------------------

The `Container` class provides a couple of convenience methods.
It can be used very similar to a dictionary::

    >>> dc = Container(items=items)
    >>> dc["content.json"]["uuid"])
    '306e2c2d-a9f6-4306-8851-1ee0fceeb852'
    >>> dc["log/console.txt"] = "Hello World!"
    >>> "log/console.txt" in dc
    True

    >>> del dc["log/console.txt"]
    >>> "log/console.txt" in dc
    False

Furthermore, the method `items()` returns a list of all full item names including the respective parts.
The method `hash()` may be used to calculate an SHA256 hash of the container content.
The hex digest of this value is stored in the attribute `hash` of the item `container.json`.

Container objects generated from an items dictionary using the parameter `items=...` are mutable, which means that you can add, modify and delete items.
As soon as you call one of the methods `write()`, `upload()`, `freeze()`, or `hash()`, the container becomes immutable.
Containers loaded from a local file or a server are immutable as well.
An immutable container will throw an exception if you try to modify its content.
However, this feature is not bulletproof.
It is not aware of any internal modifications of item objects.
You can convert an immutable container into a mutable one by calling its method `release()`.
This generates a new UUID and resets the attributes `replaces`, `created`, `modified`, `hash` and `modelVersion`.

Supported File Formats
----------------------

The container class can handle virtually any file format.
However, in order to store and read a certain file format, it needs to know how to convert the respective Python object into a bytes stream and vice versa.
File formats are identified by their file extension.
The following file extensions are currently supported by `scidatacontainer` out of the box:

.. csv-table:: 
    :header: Extension, File format, Python object, Required modules

    json, JSON file (UTF-8 encoding), dictionary or others,
    txt, Text file (UTF-8 encoding), string,
    log, Text file (UTF-8 encoding), string,
    pgm, Text file (UTF-8 encoding), string,
    png, PNG image file,  NumPy array, "cv2, numpy"
    npy, NumPy array, NumPy array, numpy
    bin, Raw binary data file, bytes,

The support for image and NumPy objects is only available when your Python environment contains the modules `cv2 <https://pypi.org/project/opencv-python/>`_ and/or `numpy <https://pypi.org/project/numpy/>`_.
The container class tries to guess the format of items with unknown extension.
However, it is more reliable to use the function `register()` to add alternative file extensions to already known file formats.
The following commands will register the extension `py` as text file::

    >>> from scidatacontainer import register
    >>> register("py", "txt")

If you want to register another Python object, you need to provide a conversion class which can convert this object to and from a bytes string. This class should be inherited from `scidatacontainer.FileBase`. The storage of NumPy arrays for example may be realized by the following code::

    >>> import io
    >>> import numpy as np
    >>> from scidatacontainer import FileBase, register

    >>> class NpyFile(FileBase):
    ...
    ...     allow_pickle = False
    ...
    ...     def encode(self):
    ...         with io.BytesIO() as fp:
    ...             np.save(fp, self.data, allow_pickle=self.allow_pickle)
    ...             fp.seek(0)
    ...             data = fp.read()
    ...         return data
    ...
    ...     def decode(self, data):
    ...         with io.BytesIO() as fp:
    ...             fp.write(data)
    ...             fp.seek(0)
    ...             self.data = np.load(fp, allow_pickle=self.allow_pickle)

    >>> register("npy", NpyFile, np.ndarray)

The third argument of the function `register()` sets this conversion class as default for NumPy array objects overriding any previous default class.
This argument is optional.

Hash values are usually derived from the bytes string of an encoded object.
If you require a different behaviour, you may also override the method `hash()` of `FileBase`.
