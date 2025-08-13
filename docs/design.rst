======
Design
======

The architecture of a NeXus file resembles the structure of xarray *DataTrees* and *Datasets*, with some important differences.
In the following it is assumed the reader is familiar with the nomenclature of `xarray <http://xarray.pydata.org/en/stable/data-structures.html>`_ and `NeXus NXdata <https://manual.nexusformat.org/classes/base_classes/NXdata.html>`_.

The following table summarize the correspondence brought by nxarray between NeXus and xarray objects and definitions.

====================    ====================
NeXus                   xarray
====================    ====================
``NXroot``              ``DataTree``
``NXentry``             ``Dataset.NXtree`` (*)
``NXdata.entries``      ``Dataset.data_vars, Dataset.coords`` (**)
*signal*                *data variable*
``NXdata.nxaxes``       ``Dataset.dims``
*axes*                  *dimensions*
====================    ====================

(*) The complete structure of the NXentry is loaded into the ``NXtree`` Dataset attribute, with the exception of the entries in ``NXdata.entries`` which are loaded into the Dataset *data variables* and *coordinates* as DataArrays (see below).

(**) The entries in ``NXdata.entries`` are loaded into the Dataset *data variables* and *coordinates* as DataArrays, provided the attributes ``@signal`` and ``@axes`` are present in the *NXdata* group. *NXlinks* are resolved transparently and are kept when saving back to NeXus. The entry attributes are assigned to the correspondent DataArray. Additionally, the ``nxgroup`` attribute is added to each DatArray and its value is set to the name of the *NXdata* group (``NXdata.nxname``).

The identification of an entry as *data variable* or *coordinate* is performed as follows:

* An entry referred by the ``@signal`` attribute of *NXdata* is considered a Dataset *data variable*.

* An entry is considered a *coordinate* if:
    
    * it is listed in the ``@axes`` attribute of *NXdata* or
    
    * an attribute ``AXIS_indices`` is present in the *NXdata* group
    
* Any other entry:
    
    * is considered a *data variable* if its shape matches the ``@signal`` field shape
    
    * is disregarded otherwise.
