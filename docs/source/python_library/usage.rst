Basic Usage
===========

Our simple application example generates and stores a list of random integer numbers. Parameters are quantity and range of the numbers. At first, we import the Python `random` module and our class `Container`::

    >>> import random
    >>> from scidatacontainer import Container

Then we generate a parameter dictionary and the actual test data::

    >>> p = {"quantity": 8, "minValue": 1, "maxValue": 6}
    >>> data = [random.randint(p["minValue"], p["maxValue"]) for i in range(p["quantity"])]
    >>> data
    [2, 5, 1, 3, 1, 4, 4, 4]

If a default author name and e-mail address is available as explained in the :doc:`/configuration` section, there are just two additional attributes, which you must provide. One is the type of the container and the other a title of the dataset.
Together with the raw data and the dictionary of parameters, we can now build the dictionary of container items::

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

Now we are ready to build the container, store it in a local file and get a short description of its content::

    >>> dc = Container(items=items)
    >>> dc.write("random.zdc")
    >>> dc
    Single-Step Container
        type:     myRandInt
        uuid:     306e2c2d-a9f6-4306-8851-1ee0fceeb852
        created:  2023-02-28 10:03:44 UTC
        author:   Reinhard Caspary

Feel free to check the content of the file `random.zdc` now by opening it on the operating system level.
Be reminded that the Windows Explorer requires the file extension `.zdc` to be registered first as in the :doc:`/configuration` section.
Recovering the dataset from the local file as a new container object works straight forward::

    >>> dc = Container(file="random.zdc")
    >>> dc["sim/dice.json"]
    [2, 5, 1, 3, 1, 4, 4, 4]

Server Storage
--------------

Container files can also easily be stored on and retrieved from a specific data storage server::

    >>> dc.upload()
    >>> dc = Container(uuid="306e2c2d-a9f6-4306-8851-1ee0fceeb852")

It is most convenient to store the server name or IP address and the API key in the :doc:`/configuration`. 
However, both values can also be specified as method parameters::

    >>> dc.upload(server="...", key="...")
    >>> dc = Container(uuid="306e2c2d-a9f6-4306-8851-1ee0fceeb852", server="...", key="...")

The server makes sure that UUIDs are unique.
Once uploaded, a dataset can never be modified on a server.
The only exemption are multi-step containers (see below).
In the rare case that a certain dataset needs to be replaced, the attribute `replaces` may be used in `content.json`.
Once uploaded, the server will always deliver the new dataset, even if the dataset with the old UUID is requested.
Only the owner of a dataset is allowed to replace it.
