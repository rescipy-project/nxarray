import xarray as xr
import nexusformat.nexus as nx

def to_datarr(nxdata):
    ''' Convert NeXus NXdata to an xarray DataArray
    
    This function convert the NXdata group to an
    xarray DataArray, keeping the default signal, all the axes
    and attributes.
    Any other field in the NXdata is disregarded.
    
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
    Any other group in the NXentry is disregarded.
    
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

    ## Add NXdata groups as DataArrays
    for nxname, nxdata in nxentry.entries.items():
        if isinstance(nxdata, nx.NXdata):
            ds[nxname] = to_datarr(nxdata)

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
        if k not in ["signal", "axes", "default"] + ["{}_indices".format(a) for a in nxfield.nxaxes]:
            attrs[k] = v.nxvalue

    return attrs

def load(filename):
    ''' Load a NeXus file to an xarray Dataset
    
    This function load the NXdata groups in the default NXentry
    of the NeXus file and return them as an xarray Dataset.
    Any other group in the file is disregarded.
    
    Arguments
        filename: file path to the NeXus file
    
    Returns:
        xarray Dataset
    
    Example:
        import nxarray as nxr
        
        ds = nxr.load(path/to/file.nx)
    '''

    # Open file and retrieve default nxdata
    f = nx.nxload(filename)
    nxdata = f.plottable_data

    # Get the nxentry relative to default nxdata
    # and return it as an xarray dataset
    nxentry = nxdata.nxgroup
    return to_datset(nxentry)
