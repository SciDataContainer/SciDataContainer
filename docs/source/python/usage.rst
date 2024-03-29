Basic Usage
===========

Container Objects
-----------------

As a simple application example, we generate and store a list of random integer numbers. Parameters are quantity and range of the numbers. At first, we import the Python package ``random`` module and the class ``Container`` from the package ``scidatacontainer``:

	>>> import random
	>>> from scidatacontainer import Container

Then we generate a parameter dictionary and the actual test data:

	>>> p = {"quantity": 8, "minValue": 1, "maxValue": 6}
	>>> data = [random.randint(p["minValue"], p["maxValue"]) for i in range(p["quantity"])]
	>>> data
	[2, 5, 1, 3, 1, 4, 4, 4]

If a default author name and e-mail address was made available as explained in the :doc:`/configuration` section, there are just two additional attributes, which you must provide. One is the type of the container and the other a title of the dataset. Together with the raw data and the dictionary of parameters, we can now build the dictionary of container items:

	>>> items = {
	...          "content.json": {
	...                           "containerType": {"name": "myRandInt"},
	...                          },
	...          "meta.json": {
	...                        "title": "My first set of random numbers",
	...                       },
	...          "sim/dice.json": data,
	...          "data/parameter.json": p,
	...         }

Now we are ready to build the container, store it in a local file and get a short description of its content:

	>>> dc = Container(items=items)
	>>> dc.write("random.zdc")
	>>> print(dc)
	Complete Container
		type:        myRandInt
		uuid:        306e2c2d-a9f6-4306-8851-1ee0fceeb852
		created:     2023-02-28T10:03:44+0100
		storageTime: 2023-02-28T10:03:44+0100
		author:      Reinhard Caspary

Feel free to check the content of the file ``random.zdc`` now by opening it on the operating system level. Be reminded that the Windows Explorer requires the file extension ``.zdc`` to be registered first as in the :doc:`/configuration` section.
Recovering the dataset from the local file as a new container object works straight forward:

	>>> dc = Container(file="random.zdc")
	>>> dc["sim/dice.json"]
	[2, 5, 1, 3, 1, 4, 4, 4]

Server Storage
--------------

Container files can be stored on and retrieved from a specific data storage server. If the server name and an API key was made available as explained in the :doc:`/configuration` section, upload and download of a container is as simple as:

	>>> dc.upload()
	>>> dc = Container(uuid="306e2c2d-a9f6-4306-8851-1ee0fceeb852")

The server makes sure that UUIDs are unique. Once uploaded, a container can never be modified on a server. The only exemption are `incomplete containers <../concept.html#variants>`_.

In the rare case that a certain container needs to be replaced, the attribute ``replaces`` may be used in ``content.json``. Once uploaded, the server will always deliver the new container, even if the container with the old UUID is requested. Only the owner of a container is allowed to replace it.


Timestamps
----------

You may use the function ``timestamp()`` to generate a timestamp in the format required by the ``Container`` class:

	>>> from scidatacontainer import timestamp
	>>> timestamp()
	2023-03-24T21:50:34+0100


Incomplete Containers
---------------------

As already mentioned, `incomplete containers <../concept.html#variants>`_ are a container variant which is intended for long running measurements or simulations. As long as the attribute ``complete`` in ``content.json`` has the value ``False``, a container may be uploaded repeatedly, each time replacing the container with the same UUID on the server:

	>>> items["content.json"]["complete"] = False
	>>> dc = Container(items=items)
	>>> dc.upload()
	>>> dc["content.json"]["uuid"]
	'306e2c2d-a9f6-4306-8851-1ee0fceeb852'

The server will only accept containers with increasing modification timestamps. Since the resolution of the internal timestamps is a second, you must wait at least one second before the next upload:

	>>> dc = Container(uuid="306e2c2d-a9f6-4306-8851-1ee0fceeb852")
	>>> dc["meas/newdata.json"] = newdata
	>>> dc.upload()

For the final upload, the container must be marked as being complete. This makes this container immutable:

	>>> dc = Container(uuid="306e2c2d-a9f6-4306-8851-1ee0fceeb852")
	>>> dc["meas/finaldata.json"] = finaldata
	>>> dc["content.json"]["complete"] = True
	>>> dc.upload()


Static Containers
-----------------

A `static container <../concept.html#variants>`_ is generated by calling the method ``freeze()`` of the container object. It is intended for static parameters in contrast to measurement or simulation data:

	>>> dc = Container(items=items)
	>>> dc.freeze()
	>>> print(dc)
	Static Container
		type:        myRandInt
		uuid:        2a7eb1c5-5fe8-4c92-be1d-2f1207b0d855
		hash:        bafc6813d92bd23b06b63eed035ba9b33415acc770c9128f47775ab2d55cc152
		created:     2023-03-01T21:01:20+0100
		storageTime: 2023-03-01T21:01:20+0100
		author:      Reinhard Caspary

Freezing a container will set the attribute ``static`` in ``content.json`` to ``True``, which makes this container immutable and it calculates an SHA256 hash of the container content. When you try to upload a static container and there is another static container with the same attributes ``containerType.name`` and ``hash``, the content of the current container object is silently replaced by the original one from the server.

