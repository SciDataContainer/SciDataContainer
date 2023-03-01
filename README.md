# scidatacontainer

This is a Python 3 implementation of a lean container class for the storage of scientific data, in a way compliant to the [FAIR princples](https://en.wikipedia.org/wiki/FAIR_data) of modern research data management. In a standardized container file it provides maximum flexibility and minimal restrictions. Data containers may be stored as local files and uploaded to a data storage server. The class is operating system independent.

The basic concept of the data container is that it keeps the raw dataset, parameter data and meta data together. Parameter data is every data which is traditionally recorded in lab books like test setup, measurement settings, simulation parameters or evaluation parameters. The idea is to make each dataset self-contained. Large amounts of parameter data may be stored in their own container, referenced by its identifier. This is especially useful for static data.

## Install

The easiest way to install the latest version of `scidatacontainer` is using PIP:
```
>>> pip install scidatacontainer
```

You find the source code together with test files some more on [GitHub](https://github.com/reincas/scidatacontainer).

## Structure and Terms

Each data container is identified by a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier), which is usually generated automatically. The *Container* file is a [ZIP package file](https://en.wikipedia.org/wiki/ZIP_(file_format)). The data in the container is stored in *Items* (file in ZIP package), which are organized in *Parts* (folder in ZIP package). The standard file extension of the container files is `.zdc`. When you execute the file `zdc.reg` on Microsoft Windows, the operating sytem treats this extension in the same way as `.zip`. This allows to inspect the file with a double-click in the Windows Explorer.

There are no restrictions regarding data formats, but items should be represented as Python dictionaries and stored as JSON files in the ZIP package, if possible. This allows to inspect, use and even create data container files with the tools provided by the operating system without any special software. However, this container class makes these tasks much more convenient. Data *Attributes* are keys of JSON mappings.

Just two items `content.json` and `meta.json` are required and must be located in the root part of the container. All data payload and parameter data should be stored in an optional set of suggested parts.

## Container Parameters

The parameters describing the container are stored in the required root item `content.json`. The following set of attributes is currently defined for this item:

- `uuid`: automatic UUID
- `replaces`: optional UUID of the predecessor of this dataset
- `containerType`: required container type mapping
    + `name`: required container name (no white space)
    + `id`: optional identifier for standardized containers
    + `version`: required standard version, if `id` is given
- `created`: automatic creation timestamp
- `modified`: automatic last modification timestamp
- `static`: required boolean flag (static datasets)
- `complete`: required boolean flag (multi-step datasets)
- `hash`: optional hex digest of SHA256 hash, required for static datasets
- `usedSoftware`: optional list of software mappings
    + `name`: required software name
    + `version`: required software version
    + `id`: optional software identifier (e.g. UUID of URL)
    + `idType`: required type of identifier, if `id` is given
- `modelVersion`: automatic data model version

## Description of Data

The meta data describing the data payload of the container is stored in the required root item `meta.json`. The following set of attributes is currently defined for this item:

- `author`: required name of the author
- `email`: required e-mail address of the author
- `comment`: optional comments on the dataset
- `title`: required title of the dataset
- `keywords`: optional list of keywords
- `description`: optional description of the dataset (abstract)

In order to simplify the generation of meta data, the data container class will insert default values for the author name and e-mail address. These default values are either been taken from the environment variables `DC_AUTHOR` and `DC_EMAIL` or fron a configuration file. This configuraton file is `%USERPROFILE%\scidata.cfg` on Microsoft Windows and `~/.scidata` on other operating systems. The file is expected to be a text file. Leading and trailing white space is ignored, as well as lines starting with `#`. The parameters are taken from lines in the form `<key>=<value>`, with the keywords `author` and `email`. Optional white space before and after the equal sign is ignored. The keywords are case-insensitive.

## Suggested Parts

Standardization simplifies data exchange as well as reuse of data. Therefore, it is suggested to store the data payload of a container in the following part structure:

- `/info`: informative parameters
- `/sim`: raw simulation results
- `/meas`: raw measurement results
- `/data`: parameters and data required to achieve results in `/sim` or `/meas`
- `/eval`: evaluation results derived from `/sim` and/or `/meas`
- `/log`: log files or other unstructured data

## Basic Usage

Our simple application example just generates and stores a list of random integer numbers. Parameters are quantity and range of the numbers. At first we import the Python `random` module and our class `Container`:
```
>>> import random
>>> from scidatacontainer import Container
```

Then we generate a parameter dictionary and the actual test data:
```
>>> p = {"quantity": 8, "minValue": 1, "maxValue": 6}
>>> data = [random.randint(p["minValue"], p["maxValue"]) for i in range(p["quantity"])]
>>> data
[2, 5, 1, 3, 1, 4, 4, 4]
```

If a default author name and e-mail address is available as explained above, there are just two aditional attributes which you must provide. One is the the type of the container and the other a title of the dataset. Together with the raw data and the dictionary of parameters we can now build the dictionary of container items:
```
>>> items = {
    "content.json": {
        "containerType": {"name": "myRandInt"},
        },
    "meta.json": {
        "title": "My first set of random numbers",
        },
    "sim/dice.json": data,
    "data/parameter.json": p,
    }
```

Now we are ready to build the container, store it in a local file and get a short description of its content:
```
>>> dc = Container(items=items)
>>> dc.write("random.zdc")
>>> dc
Single-Step Container
  type:     myRandInt
  uuid:     306e2c2d-a9f6-4306-8851-1ee0fceeb852
  created:  2023-02-28 10:03:44 UTC
  author:   Reinhard Caspary
```

Feel free to check the content of the file `random.zdc` now by opening it on the operating system level. Be reminded that the Windows Explorer requires the file extension `.zdc` to be registered first as explained above. Recovering the dataset from the local file as a new container object works staight forward:
```
>>> dc = Container(file="random.zdc")
>>> dc["sim/dice.json"]
[2, 5, 1, 3, 1, 4, 4, 4]
```

## Server Storage

Container files can also easily be stored on and retrieved from a specific data storage server:
```
>>> dc.upload()
>>> dc = Container(uuid="306e2c2d-a9f6-4306-8851-1ee0fceeb852")
```

In order to be able to use the server, you need an account. This enables you to get an API key. It is most convenient to store the server name or IP address and the API key in the configuration file mentioned above (keywords `server` and `key`) or in the environment variables `DC_SERVER` and `DC_KEY`. Both values can also be specified as method parameters:
```
>>> dc.upload(server="...", key="...")
>>> dc = Container(uuid="306e2c2d-a9f6-4306-8851-1ee0fceeb852", server="...", key="...")
```

The server makes sure that UUIDs are unique. Once uploaded, a dataset can never be modified on a server. The only exemption are multi-step containers, see below. In the rare case that a certain dataset needs to be replaced, the attribute `replaces` may be used in `content.json`. Once uploaded, the server will always deliver the new dataset, even if the dataset with the old UUID is requested. Replacing is only allowed for the owner of a dataset.

Three different types of containers are currently supported, which differ mainly in the way they are handled by the storage server. The standard one is the **single-step container**. The second one is a **multi-step container**, which is intended for long running measurements or simulations. As long as the attribute `complete` in `content.json` has the value `False`, the dataset may be uploaded repeatedly, each time replacing the dataset with the same UUID:
```
>>> items["content.json"]["complete"] = False
>>> dc = Container(items=items)
>>> dc.upload()
>>> dc["content.json"]["uuid"]
306e2c2d-a9f6-4306-8851-1ee0fceeb852
```

The server will only accept containers with increasing modification timestamps. Since the resolution of the internal timestamps is a second, you must wait at least one second before the next step:
```
>>> dc = Container(uuid="306e2c2d-a9f6-4306-8851-1ee0fceeb852")
>>> dc["meas/newdata.json"] = newdata
>>> dc.upload()
```

For the final step, the upload must be marked as beeing complete. This makes this dataset immutable:
```
>>> dc = Container(uuid="306e2c2d-a9f6-4306-8851-1ee0fceeb852")
>>> dc["meas/finaldata.json"] = finaldata
>>> dc["content.json"]["complete"] = True
>>> dc.upload()
```

The third container type is a **static container**. Static containers are intended for static parameters in contrast to measurement or simulation data. An example would be a detailed description of a measurement setup, which is used for many measurements. Instead of including the large setup data with each single measurement dataset, the whole setup may be stored as a single static dataset and referenced by its UUID in the measurement datasets.

A static container is generated by calling the method `freeze()` of the container object:
```
>>> dc = Container(items=items)
>>> dc.freeze()
>>> dc
Static Container
  type:     myRandInt
  uuid:     2a7eb1c5-5fe8-4c92-be1d-2f1207b0d855
  hash:     bafc6813d92bd23b06b63eed035ba9b33415acc770c9128f47775ab2d55cc152
  created:  2023-03-01 21:01:20 UTC
  author:   Reinhard Caspary
```

Freezing a container sets the attribute `static` in `content.json` to `True`, which makes this container immutable and it calculates a hash value of the container content. When a second static container with the same hash value is uploaded to the server, it responds with an error code in order to avoid the storage of redundant data.

## Convenience Methods

The `Container` class provides a couple of convenience methods. It can be used very similar to a dictionary:
```
>>> dc = Container(items=items)
>>> dc["content.json"]["uuid"]
306e2c2d-a9f6-4306-8851-1ee0fceeb852
>>> dc["log/console.txt"] = "Hello World!"
>>> "log/console.txt" in dc
True
>>> del dc["log/console.txt"]
>>> "log/console.txt" in dc
False
```