=====
Usage
=====
The recommended import::

    import nxarray as nxr


To save a DataArray or Dataset to a NeXus file use the
nxr.save() method::

    dr = xarray.DataArray()
    dr.nxr.save(path/to/file.nx)


To load a NeXus file into an xarray Dataset use the
nxr.load() function::

    ds = nxr.load(path/to/file.nx)
