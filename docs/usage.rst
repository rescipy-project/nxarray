=====
Usage
=====

After installation, the recommended import is:

.. code-block:: python
    
    import nxarray as nxr


Now the ``nxr.save()`` method will be available to xarray objects. To save an existing *DataArray* or *Dataset* to a NeXus file simply use it with:

.. code-block:: python
    
    dr = xarray.DataArray()
    dr.nxr.save('path/to/file.nx')
    
    ds = xarray.Dataset()
    ds.nxr.save('path/to/file.nx')


To load a NeXus file into an xarray *Dataset* use the ``nxr.load()`` function:

.. code-block:: python
    
    ds = nxr.load('path/to/file.nx')

The default NXentry in the NeXus file will be loaded, with all its subgroups (NXdata, NXinstrument, NXsample...).
To load an NXentry other than the default one, use the ``entry=`` argument.


Examples
========

Let's start by importing:

.. code-block:: python
    
    import numpy as np
    import xarray as xr
    import nxarray as nxr


and creating a dataset ``ds``:

.. code-block:: python
    
    ds = xr.Dataset()
    data = xr.DataArray(np.random.randn(2, 3),
                        dims=('x', 'y'),
                        coords={'x': [10, 20], 'y': [1,2,3]},
                        name='some_data')
    ds['MyData'] = data

The ``ds`` *Dataset* can be saved to a NeXus file to disk simply with:

.. code-block:: python
    
    ds.nxr.save('ds.nxs')

You can load it back, let's say to another *Dataset* ``my_ds`` with:

.. code-block:: python
    
    my_ds = nxr.load('ds.nxs')

and you can check that the whole structure of your *Dataset* is the same.

A *DataArray* can also be saved to a NeXus file. In this case, a *Dataset*, with your *DataArray* inside, will be automatically created and saved to file. For example the ``data`` *DataArray* of the previous example can be equally saved with:

.. code-block:: python
    
    data.nxr.save('data.nxs')

This time, when you will load it back, a *Dataset* will be returned, with your original *DataArray* inside it:

.. code-block:: python
    
    my_ds2 = nxr.load('data.nxs')
    my_data2 = ds2['some_data']


Naming conventions
==================

Note that the ``nxr`` accessor for xarray objects will always be available with this naming, i.e. ``nxr.save()`` will be used independently of the shorthand used when import nxarray.

On the other hand, ``nxarray`` methods naming will depend on the import statement, *i.e.* when using just ``import nxarray``, ``load()`` will be available with ``nxarray.load()`` and *not* with ``nxr.load()``.
