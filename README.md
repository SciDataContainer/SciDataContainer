# SciDataContainer

This is a lean container file format for scientific data, in a way compliant to the [FAIR principles](https://en.wikipedia.org/wiki/FAIR_data) of modern research data management. Using a standardized container file it provides maximum flexibility and minimal restrictions for scientists working in the lab or performing simulations. Data containers may be stored as local files or uploaded to a data storage server. The container is based on the well-known ZIP format and thus independent of the operating system as well as programming languages. This makes this container a perfect choice for the publication of scientific data in online repositories.

## Documentation

[![Sphinx Docs](https://github.com/SciDataContainer/SciDataContainer/actions/workflows/sphinx-docs.yml/badge.svg)](https://github.com/SciDataContainer/SciDataContainer/actions/workflows/sphinx-docs.yml)

The full [documentation](https://scidatacontainer.readthedocs.io/en/latest/) together with all supported language implementations is hosted on [Read the Docs](https://readthedocs.org/).

## Implementations

Currently there is only a [Python 3](https://www.python.org/) implementation available, which you find in the folder `python`. Please contact us, if you are interested in implementing a library for another programming language. We are already on the way to build an operation system independent GUI to simplify the usage of the container format outside a programming environment.

## Server

The data storage server for SciDataContainers is currently developed. Access to a test server is available for [PhoenixD](https://www.phoenixd.uni-hannover.de) members. We will make the source code of the server publicly available as soon as possible. If you are from outside PhoenixD and wish to get early access, you are welcome. Please contact us.

## Acknowledgement

This is a project of the cluster of Excellence [PhoenixD](https://www.phoenixd.uni-hannover.de) funded by the Deutsche Forschungsgemeinschaft ([DFG](https://www.dfg.de/en/), German Research Foundation) under Germany’s [Excellence Strategy](https://www.dfg.de/en/research_funding/programmes/excellence_strategy/index.html) (EXC 2122, Project ID 390833453).

