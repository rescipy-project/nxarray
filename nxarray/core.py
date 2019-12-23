import xarray as xr
import nexusformat.nexus as nx

def to_datarr(nxdata):
    ''' Convert NeXus NXdata to xarray DataArray
    
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
    if nxdata.nxsignal:
        data = nxdata.nxsignal.nxdata
        name = nxdata.nxsignal.nxname
    else:
        return None

    ## Generate coordinates dictionary
    coords = {}
    for axes in nxdata.nxaxes:
        coords[axes.nxname] = axes.nxdata

    ## Retrieve dimensions
    dims = nxdata.attrs["axes"]

    ## Retrieve attributes
    attrs = nxdata.attrs
    # Remove attributes specific to NXdata
    for k in [name, "axes"] + ["{}_indices".format(a) for a in nxdata.nxaxes]:
        if k in attrs:
            del attrs[k]

    # Create xarray DataArray
    datarr = xr.DataArray(data,
                          name=name,
                          coords=coords,
                          dims=dims,
                          attrs=attrs)

    return datarr

def to_datset(nxentry):
    ''' Convert NeXus NXentry to xarray Dataset
    
    Arguments
        nxentry: NeXus NXentry to convert
    
    Returns:
        xarray Dataset
    
    Example:
        import nxarray as nxr
        
        nxentry = nexus.NXentry()
        ds = nxr.to_datset(nxentry)
    '''

    ds = xr.Dataset()

    for nxname, nxdata in nxentry.entries.items():
        if isinstance(nxdata, nx.NXdata):
            ds[nxname] = to_datarr(nxdata)

    return ds

def load(filename):
    ''' Load a NeXus file to xarray Dataset
    
    This function load the default NXentry in the NeXus file
    and return it as xarray dataset.
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
    default = f.plottable_data

    # Get nxentry relative to default nxdata
    # and return it as xarray dataset
    nxentry = default.nxgroup
    return to_datset(nxentry)
