=====
Usage
=====

After installation, the recommended import is:

.. code-block:: python
    
    import nxarray as nxr


To save an existing *DataArray* or *Dataset* to a NeXus file simply use the ``nxr.save()`` method:

.. code-block:: python
    
    dr = xarray.DataArray()
    dr.nxr.save('path/to/file.nx')
    
    ds = xarray.Dataset()
    ds.nxr.save('path/to/file.nx')


To load a NeXus file into an xarray *Dataset* use the ``nxr.load()`` function:

.. code-block:: python
    
    ds = nxr.load('path/to/file.nx')
