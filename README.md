# scidatacontainer

This is a Python 3 implementation of a lean container class for the storage of scientific data, in a way compliant to the [FAIR princples](https://en.wikipedia.org/wiki/FAIR_data) of modern research data management. In a standardized container file it provides maximum flexibility and minimal restrictions. Data containers may be stored as local files and uploaded to a data storage server. The class is operating system independent.

The basic concept of the data container is that it keeps the raw dataset, parameter data and meta data together. Parameter data is every data which is traditionally recorded in lab books like test setup, measurement settings, simulation parameters or evaluation parameters. The idea is to make each dataset self-contained. Large amounts of parameter data may be stored in their own container, referenced by its identifier. This is especially useful for static data.

## Structure and Terms

Each data container is identified by a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier), which is usually generated automatically. The *Container* file is a [ZIP package file](https://en.wikipedia.org/wiki/ZIP_(file_format)). The data in the container is contained in *Items* (file in ZIP package), which are organized in *Parts* (folder in ZIP package). The standard file extension of the container files is `.zdc`. When you execute the file `zdc.reg` on Microsoft Windows, the operating sytem treats this extension in the same way as `.zip`. This allows to inspect the file with a double-click in the Windows Explorer.

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

In order to simplify the generation of meta data, the data container class will insert default values for the author name and e-mail address. These default values are either been taken from the environment variables `DC_AUTHOR` and `DC_EMAIL` or fron a configuration file. This configuraton file is `%HOMEDRIVE%%HOMEPATH\scidata.cfg%` on Microsoft Windows and `~/.scidata` on other operating systems. The file is expected to be a text file. Leading and trailing white space is ignored, as well as lines starting with `#`. The parameters are taken from lines in the form `<key>=<value>`, with the keywords `author` and `email`. Optional white space before and after the equal sign is ignored. The keywords are case-insensitive.

## Suggested Parts

Standardization simplifies data exchange as well as reuse of data. Therefore, it is suggested to store the data payload of a container in the following part structure:

- `/info`: informative parameters
- `/sim`: raw simulation results
- `/meas`: raw measurement results
- `/data`: parameters and data required to achieve results in `/sim` or `/meas`
- `/eval`: evaluation results derived from `/sim` and/or `/meas`
- `/log`: log files or other unstructured data

## Usage

Our simple application sample is that we generate a list of random integer numbers. Parameters are quantity and range of the numbers. At first we import the Python `random` module and our class `Container`:
```
import random
from scidatacontainer import Container
```

Then we generate a parameter dictionary and the actual test data:
```
p = {"quantity": 8, "minValue": 1, "maxValue": 6}
data = [random.randint(p["minValue"], p["maxValue"]) for i in range(p["quantity"])]
```

If a default author name and e-mail address is available, there are just two aditional attributes which you must provide. One is the the type of the container and a title of the dataset. Together with the raw data and the dictionary of parameters we build the dictionary of container items:
```
items = {
    "content.json": {
        "containerType": {"name": "myRandInt"},
        },
    "meta.json": {
        "title": "My first set of random numbers",
        },
    "meas/dice.json": data,
    "data/parameter.json": p,
    }
```

aaa