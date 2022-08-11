=======
nxarray
=======

**A software package for NeXus/HDF5 conversion from and to Python xarray.**

``nxarray`` extends xarray *DataArrays* and *Datasets* with a high-level python interface for NeXus/HDF5 file input and output.


.. toctree::
   :caption: Contents
   :maxdepth: 1
   
   installation
   usage
   design


Motivations
===========

`xarray <https://xarray.dev/>`_ is the most used Python package for labeled multi-dimensional data handling, providing convenient data structures (namely *DataArrays* and *Datasets*) and including a large library of functions for advanced analytics and visualization with these data structures.

Despite xarray supports natively import/export of `HDF5 <https://www.hdfgroup.org/solutions/hdf5/>`_ (a file format designed to efficiently store and organize large amount of data), it does not provide an integrated interface to the `NeXus file format <https://www.nexusformat.org/>`_, the standard *de facto* for scientific data storage, based on HDF5 and increasingly adopted in `laboratories and large-scale facilities <https://www.nexusformat.org/Facilities.html>`_ all over the world.

With this respect, the `nxarray <https://nxarray.readthedocs.io/en/latest/>`_ package comes into play, bridging xarray with the NeXus format. This package actually extends xarray, providing convenient loading and saving methods for NeXus files, directly to *Datasets* objects. The architecture of a NeXus file resembles the structure of an xarray *Dataset*, and indeed both of them are specifically designed for handling scientific data with its relevant metadata.

``nxarray`` is part of the `reScipy project <https://rescipy-project.readthedocs.io>`_.


Feedback
========

Please report any feedback, bugs, or feature requests by opening an issue on the `issue tracker <https://github.com/rescipy-project/nxarray/issues>`_ of the code repository. You should provide as much information as possible to reproduce the problem, and details of your desiderata.
