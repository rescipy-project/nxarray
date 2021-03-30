import xarray as xr
import nexusformat.nexus as nx

def to_datarr(nxdata):
    ''' Convert NeXus NXdata to an xarray DataArray
    
    This function convert the NXdata group to an
    xarray DataArray, keeping the @default signal, all the axes
    and attributes.
    
    Arguments
        nxdata: NeXus NXdata to convert
    
    Returns:
        xarray DataArray
    
    Example:
        import nxarray as nxr
        
        nxdata = nexus.NXdata()
        dr = nxr.to_datarr(nxdata)
    '''

    ## Retrieve data and name
    data = nxdata.nxsignal.nxdata
    name = nxdata.nxsignal.nxname

    ## Generate coordinates dictionary
    coords = {}
    for axes in nxdata.nxaxes:
        coords[axes.nxname] = axes.nxdata

    ## Retrieve dimensions
    dims = nxdata.attrs["axes"]

    ## Add NXdata and NXsignal attributes to the DataArray
    attrs = {**_get_attrs(nxdata),
             **_get_attrs(nxdata.nxsignal)}

    # Create the xarray DataArray
    datarr = xr.DataArray(data,
                          name=name,
                          coords=coords,
                          dims=dims,
                          attrs=attrs)

    return datarr

def to_datset(nxentry):
    ''' Convert NeXus NXentry to an xarray Dataset
    
    This function convert the NXdata groups in the NXentry
    to DataArrays of an xarray Dataset.
    Other groups in the NXentry are saved in the Dataset attribute "NX" as a dictionary.
    
    Arguments
        nxentry: NeXus NXentry to convert
    
    Returns:
        xarray Dataset
    
    Example:
        import nxarray as nxr
        
        nxentry = nexus.NXentry()
        ds = nxr.to_datset(nxentry)
    '''

    ## Initialize Dataset
    ds = xr.Dataset()

    ## Add NeXus objects to the Dataset
    ds.attrs["NX"] = dict()
    for nxname, nxobject in nxentry.entries.items():
        if isinstance(nxobject, nx.NXdata):
            # Add NXdata groups as DataArrays
            ds[nxname] = to_datarr(nxobject)
        else:
            # Retrieve other NeXus groups in a dictionary
            ds.attrs["NX"][nxname] = nxobject

    ## Add NXentry attributes to the Dataset
    attrs = _get_attrs(nxentry)

    return ds

def _get_attrs(nxfield):
    ''' Convert dictionary of NXattr to a common dictionary
    '''

    # Initialize attributes dictionary
    attrs = {}

    # Loop over NXattr dictionary
    # skipping some attributes specific to NXfield
    for k,v in nxfield.attrs.items():
        try:
            axes_indices = list("{}_indices".format(a) for a in nxfield.nxaxes)
        except TypeError:
            axes_indices = list()
        if k not in ["signal", "axes", "default"] + axes_indices:
            attrs[k] = v.nxvalue

    return attrs

def load(filename, entry=None):
    ''' Load a NeXus file to an xarray Dataset
    
    This function load the NXdata groups in the given NXentry
    of the NeXus file and return them as an xarray Dataset.
    Other groups in the NXentry are saved in the Dataset attribute "NX" as a dictionary.
    Only one NXentry can be loaded from the NeXus file (by default the @default one).
    
    Arguments
        filename: file path to the NeXus file
        entry (optional): name of the NXentry to be loaded. If None the @default NXentry will be loaded.
    
    Returns:
        xarray Dataset
    
    Example:
        import nxarray as nxr
        
        ds = nxr.load(path/to/file.nx)
    '''

    # Open NeXus file
    f = nx.nxload(filename)

    # Get the nxentry and return it as an xarray dataset
    if entry:
        nxentry = f[entry]
    else:
        # Get the nxentry relative to @default nxdata
        nxdata = f.plottable_data
        nxentry = nxdata.nxgroup

    return to_datset(nxentry)
