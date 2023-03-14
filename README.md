# scidatacontainer

This is the Python 3 implementation of a lean container class for the storage of scientific data, in a way compliant to the [FAIR principles](https://en.wikipedia.org/wiki/FAIR_data) of modern research data management. Using a standardized container file it provides maximum flexibility and minimal restrictions. Data containers may be stored as local files and uploaded to a data storage server. The class is operating system independent.

This is a project of the cluster of Excellence [PhoenixD](https://www.phoenixd.uni-hannover.de) and the data server is currently only available for PhoenixD members. However, we intend to make the whole project including the server publicly available. If you are from outside PhoenixD and wish to get early access, you are welcome. Please contact us.

## Install

The easiest way to install the latest version of [`scidatacontainer`](https://pypi.org/project/scidatacontainer/) is using PIP:
```
>>> pip install scidatacontainer
```

You find the source code together with test files on [GitHub](https://github.com/reincas/scidatacontainer).

## Data Container Concept

The basic concept of the data container is that it keeps the raw dataset, parameter data and meta data together. Parameter data is every data which is traditionally recorded in lab books like test setup, measurement settings, simulation parameters or evaluation parameters. The idea is to make each dataset self-contained.

Each data container is identified by a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier), which is usually generated automatically. The **Container** file is a [ZIP package file](https://en.wikipedia.org/wiki/ZIP_(file_format)). The data in the container is stored in **Items** (files in ZIP package), which are organized in **Parts** (folders in ZIP package). The standard file extension of the container files is `.zdc`.

On Microsoft Windows you may inspect ZDC files with a double-click in the Windows Explorer. This requires that you register the extension `.zdc` as a copy of `.zip`. Run the following on the command prompt to achieve this behaviour:
```
>>> reg copy HKCR\.zip HKCR\.zdc /s /f
```

There are no restrictions regarding data formats, but items should be represented as Python dictionaries and stored as [JSON](https://en.wikipedia.org/wiki/JSON) files in the ZIP package, whenever possible. This allows to inspect, use and even create data container files with the tools provided by the operating system without any special software. However, this container class makes these tasks much more convenient. We call the keys of JSON mappings data **Attributes**.

Only the two items `content.json` and `meta.json` are required and must be located in the root part of the container. The optional root item `license.txt` may be used to store the text of the license for the dataset. The data payload and the parameter data should be stored in an optional set of suggested parts as explained below.

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
- `organization`: optional affiliation of the author
- `comment`: optional comments on the dataset
- `title`: required title of the dataset
- `keywords`: optional list of keywords
- `description`: optional abstract for the dataset
- `created`: optional creation timestamp of the dataset
- `doi`: optional digital object identifier of the dataset
- `license`: optional data license name (e.g. ["CC-BY"](https://creativecommons.org/licenses/by/4.0/))

In order to simplify the generation of meta data, the data container class will insert default values for the author name and e-mail address. These default values are either been taken from the environment variables `DC_AUTHOR` and `DC_EMAIL` or from a configuration file. This configuraton file is `%USERPROFILE%\scidata.cfg` on Microsoft Windows and `~/.scidata` on other operating systems. The file is expected to be a text file. Leading and trailing white space is ignored, as well as lines starting with `#`. The parameters are taken from lines in the form `<key>=<value>`, with the keywords `author` and `email`. Optional white space before and after the equal sign is ignored. The keywords are case-insensitive.

The value of the attribute `created` should be a UTC timestamp string in the form `2023-02-17 15:27:00 UTC`. You may use the function `scidatacontainer.timestamp()` to generate this string.

## Suggested Parts

Standardization simplifies data exchange as well as reuse of data. Therefore, it is suggested to store the data payload of a container in the following part structure:

- `/info`: informative parameters
- `/sim`: raw simulation results
- `/meas`: raw measurement results
- `/data`: parameters and data required to achieve results in `/sim` or `/meas`
- `/eval`: evaluation results derived from `/sim` and/or `/meas`
- `/log`: log files or other unstructured data

## Basic Usage

Our simple application example just generates and stores a list of random integer numbers. Parameters are quantity and range of the numbers. At first, we import the Python `random` module and our class `Container`:
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

If a default author name and e-mail address is available as explained above, there are just two additional attributes, which you must provide. One is the type of the container and the other a title of the dataset. Together with the raw data and the dictionary of parameters, we can now build the dictionary of container items:
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

Feel free to check the content of the file `random.zdc` now by opening it on the operating system level. Be reminded that the Windows Explorer requires the file extension `.zdc` to be registered first as explained above. Recovering the dataset from the local file as a new container object works straight forward:
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

The server makes sure that UUIDs are unique. Once uploaded, a dataset can never be modified on a server. The only exemption are multi-step containers (see below). In the rare case that a certain dataset needs to be replaced, the attribute `replaces` may be used in `content.json`. Once uploaded, the server will always deliver the new dataset, even if the dataset with the old UUID is requested. Only the owner of a dataset is allowed to replace it.

Three different types of containers are currently supported, which differ mainly in the way in which they are handled by the storage server. The standard one is the **single-step container**. The second one is a **multi-step container**, which is intended for long running measurements or simulations. As long as the attribute `complete` in `content.json` has the value `False`, the dataset may be uploaded repeatedly, each time replacing the dataset with the same UUID:
```
>>> items["content.json"]["complete"] = False
>>> dc = Container(items=items)
>>> dc.upload()
>>> dc["content.json"]["uuid"]
306e2c2d-a9f6-4306-8851-1ee0fceeb852
```

The server will only accept containers with increasing modification timestamps. Since the resolution of the internal timestamps is a second, you must wait at least one second before the next upload:
```
>>> dc = Container(uuid="306e2c2d-a9f6-4306-8851-1ee0fceeb852")
>>> dc["meas/newdata.json"] = newdata
>>> dc.upload()
```

For the final upload, the container must be marked as being complete. This makes this dataset immutable:
```
>>> dc = Container(uuid="306e2c2d-a9f6-4306-8851-1ee0fceeb852")
>>> dc["meas/finaldata.json"] = finaldata
>>> dc["content.json"]["complete"] = True
>>> dc.upload()
```

The third container type is a **static container**. Static containers are intended for static parameters in contrast to measurement or simulation data. An example would be a detailed description of a measurement setup, which is used for many measurements. Instead of including the large setup data with each individual measurement dataset, the whole setup may be stored as a single static dataset and referenced by its UUID in the measurement datasets.

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

Freezing a container will set the attribute `static` in `content.json` to `True`, which makes this container immutable and it calculates an SHA256 hash of the container content. When you try to upload a static container and there is another static container with the same attributes `containerType.name` and `hash`, the content of the current container object is silently replaced by the original one from the server.

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

Furthermore, the method `items()` returns a list of all full item names including the respective parts. The method `hash()` may be used to calculate an SHA256 hash of the container content. The hex digest of this value is stored in the attribute `hash` of the item `container.json`.

The container methods `read()` and `download()` are not intended to be called directly. They are called implicity when a new container is generated with the parameters `file=...` or `uuid=...`, respectively. They replace the current content of the container.

Container objects generated from an items dictionary using the parameter `items=...` are mutable, which means that you can add, modify and delete items. As soon as you call one of the methods `write()`, `upload()`, `freeze()`, or `hash()`, the container becomes immutable. Containers loaded from a local file or a server are immutable as well. An immutable container will throw an exception if you try to modify its content. However, this feature is not bulletproof. It is not aware of any internal modifications of item objects. You can convert an immutable container into a mutable one by calling its method `release()`. This generates a new UUID and resets the attributes `replaces`, `created`, `modified`, `hash` and `modelVersion`.

## File Formats

The container class can handle virtually any file format. However, in order to store and read a file format, it needs to know how to convert the respective Python object into a bytes stream and vice versa. File formats are identified by their file extension. The following file extentions are currently supported by `scidatacontainer` out of the box:

| Extension | File format | Python object | Required modules |
| --- | --- | --- | --- |
| json | JSON file (UTF-8 encoding) | dictionary | |
| txt | Text file (UTF-8 encoding) | string | |
| log | Text file (UTF-8 encoding) | string | |
| pgm | Text file (UTF-8 encoding) | string | |
| png | PNG image file | NumPy array | cv2, numpy |
| npy | NumPy array | NumPy array | numpy |
| bin | Raw binary data file | bytes | |

The support for image and NumPy objects is only available when your Python environment contains the modules [`cv2`](https://pypi.org/project/opencv-python/) and/or [`numpy`](https://pypi.org/project/numpy/). The container class tries to guess the format of items with unknown extension. However, it is more reliable to use the function `register()` to add alternative file extensions. The following commands will register the extension `py` as text file:
```
>>> from scidatacontainer import register
>>> register("py", "txt")
```

If you want to register another Python object, you need to provide a conversion class which can convert this object to and from a bytes string. This class should be inherited from `scidatacontainer.FileBase`. The storage of NumPy arrays for example may be realized by the following code
```
import io
import numpy as np
from scidatacontainer import FileBase, register

class NpyFile(FileBase):

    allow_pickle = False

    def encode(self):
        with io.BytesIO() as fp:
            np.save(fp, self.data, allow_pickle=self.allow_pickle)
            fp.seek(0)
            data = fp.read()
        return data

    def decode(self, data):
        with io.BytesIO() as fp:
            fp.write(data)
            fp.seek(0)
            self.data = np.load(fp, allow_pickle=self.allow_pickle)

register("npy", NpyFile, np.ndarray)
```

The third argument of the function `register()` sets this conversion class as default for NumPy array objects overriding any previous default class. This argument is optional.

Hash values are usually derived from the bytes string of an encoded object. If you require a different behaviour, you may also override the method `hash()` of the conversion class.