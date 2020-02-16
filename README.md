# nxarray

xarray extension for NeXus input/output.

Introduction
============
nxarray extends xarray DatArrays and Datasets with a high-level
python interface for NeXus file input and output.

Installation
============

```
    pip install nxarray
```

Prerequisites
=============
nxarray is built on and depends on nexusformat and xarray.

* [nexusformat](https://github.com/nexpy/nexusformat)
* [xarray](http://xarray.pydata.org)

Usage
=====
The recommended import

```
    import nxarray as nxr
```

To save a DataArray or Dataset to a NeXus file use the
nxr.save() method:

```
    dr = xarray.DataArray()
    dr.nxr.save(path/to/file.nx)
```

To load a NeXus file into an xarray Dataset use the
nxr.load() function:

```
    ds = nxr.load(path/to/file.nx)
```
See the docstring help for more detailed information.
