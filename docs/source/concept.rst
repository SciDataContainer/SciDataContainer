Data Container Concept
======================

The basic concept of the data container is that it keeps the raw dataset, parameter data and meta data together. Parameter data is every data which scientists traditionally record in lab books like a description of the test setup, measurement settings, simulation parameters or evaluation parameters.
The idea is to make each dataset self-contained.
Each data container is identified by a `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`_, which is usually generated automatically.
The **Container** file is a `ZIP package file <https://en.wikipedia.org/wiki/ZIP_(file_format)>`_.
The data in the container is stored in **Items** (files in ZIP package), which are organized in **Parts** (folders in ZIP package).
The standard file extension of the container files is `.zdc`.

There are no restrictions regarding data formats inside the container, but items should be represented as Python dictionaries and stored as `JSON <https://en.wikipedia.org/wiki/JSON>`_ files in the ZIP package, whenever possible.
This allows to inspect, use and even create data container files with the tools provided by the operating system without any special software.
However, this container class makes these tasks much more convenient for Python programmers.
We call the keys of JSON mappings data **Attributes**.
Only the two items `content.json` and `meta.json` are required and must be located in the root part of the container. The optional root item `license.txt` may be used to store the text of the license for the dataset.
The data payload and the parameter data should be stored in an optional set of suggested parts as explained below.

Container Parameters
--------------------
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
    + `id`: optional software identifier (e.g. UUID or URL)
    + `idType`: required type of identifier, if `id` is given
- `modelVersion`: automatic data model version

Description of Data
-------------------

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
- `license`: optional data license name (e.g. `"MIT" <https://en.wikipedia.org/wiki/MIT_License>`_ or `"CC-BY" <https://creativecommons.org/licenses/by/4.0/>`_)

In order to simplify the generation of meta data, the data container class will try to insert default values for the author name and e-mail address (see :doc:`configuration`).
The value of the attribute `created` should be a UTC timestamp string in the form `2023-02-17 15:27:00 UTC`. You may use the function `scidatacontainer.timestamp()` to generate this string.

Suggested Parts
---------------

Standardization simplifies data exchange as well as reuse of data. Therefore, it is suggested to store the data payload of a container in the following part structure:

- `/info`: informative parameters
- `/sim`: raw simulation results
- `/meas`: raw measurement results
- `/data`: parameters and data required to achieve results in `/sim` or `/meas`
- `/eval`: evaluation results derived from `/sim` and/or `/meas`
- `/log`: log files or other unstructured data
