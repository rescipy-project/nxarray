=====
Usage
=====

After installation, import nxarray with:
    
>>> import nxarray


Now the ``nxr.save()`` method will be available to xarray *Datasets*. To save an existing *Dataset* to a NeXus file simply type:
    
>>> ds = xarray.Dataset()
>>> ds.nxr.save('path/to/file.nx')


To load a NeXus file into an xarray *Dataset* use the ``nxarray.load()`` function:
    
>>> ds = nxarray.load('path/to/file.nx')

The default *NXentry* in the NeXus file will be loaded into the *Dataset*, with all its subgroups (*NXdata*, *NXinstrument*, *NXsample*...).

Note that just a single *NXentry* at once can be loaded into a *Dataset*. To load a different *NXentry*, specify it using the ``entry=`` argument:
    
>>> ds = nxarray.load('path/to/file.nx', entry="myentry")

Upon loading, the fields in the *NXdata* groups within the *NXentry* are loaded into *data variable* and *coordinates* of the dataset, with their relevant attributes:

>>> ds


The NeXus tree of the *NXentry* with all the subgroups (*NXinstrument*, *NXsample*...) is stored in the ``NXtree`` attribute of the *Dataset* (TAB completion can be used on ``NXtree``).
    
>>> ds.NXtree
    data:NXdata
      @axes = 'energy'
      @energy_indices = 0
      @signal = 'absorbed_beam'
    instrument:NXinstrument
      source:NXsource
      current = 308.52
        @units = 'mA'

>>> ds.NXtree.instrument
    NXinstrument('instrument')


All xarray methods and attributes are accesible as usual. E.g. to plot the default signal:

>>> ds.absorbed_beam.plot()

For more info on the resulting *Dataset* structure and the architecture of ``nxarray`` look at the :doc:`Design section </design>`.


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

You can load it back, let's say to another *Dataset* ``ds2`` with:

.. code-block:: python
    
    ds2 = nxarray.load('ds.nxs')

and you can check that the whole structure of your *Dataset* is preserved.
Additionally, the ``NXtree`` attribute is present (in this example containing zero objects).


Naming conventions
==================

Note that the ``nxr`` accessor for xarray objects will always be available with this naming, independently of the shorthand used when import nxarray.
