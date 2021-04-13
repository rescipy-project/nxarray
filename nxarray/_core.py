import xarray as xr
import nexusformat.nexus as nx

def _to_datarrs(nxdata):
    ''' Convert NeXus NXdata to xarray data variables and coordinates
    
    This function convert the NXdata group to xarray data variables
    and coordinates, keeping the @default signal, all the axes
    and attributes.
    
    Arguments
        nxdata: NeXus NXdata to convert
    
    Returns:
        tuple of data variables list and coordinates list
    '''

    ## Check @signal and @axes attributes exist
    if any(attr not in nxdata.attrs for attr in ["signal", "axes"]):
        return list(), list()

    ## Retrieve signal data and name
    signal_name = nxdata.attrs["signal"]
    signal_data = nxdata[signal_name].nxdata

    ## Retrieve dimensions
    axes = nxdata.attrs["axes"]
    if isinstance(axes, str):
        axes = [axes]

    ## Data variables and coordinates lists
    data_vars = list()
    coords = list()

    # Cycle over NXgroup entries
    for entry in nxdata.entries:

        # ENTRY is the default signal
        if entry == signal_name:
            # Collect NXdata and NXsignal attributes
            attrs = _get_attrs(nxdata[entry])
            datarr = xr.DataArray(nxdata[entry].nxdata,
                                  name=entry,
                                  dims=axes,
                                  attrs=attrs)

            # Set NXdata and NXlink attributes
            datarr.attrs["nxgroup"] = nxdata.nxname
            if isinstance(nxdata[entry], nx.NXlink):
                datarr.attrs["target"] = nxdata[entry].nxlink.nxpath

            # Add signal datarr to data_vars list
            data_vars.append(datarr)

        # ENTRY is listed as an axes
        elif entry in axes:
            attrs = _get_attrs(nxdata[entry])
            datarr = xr.DataArray(nxdata[entry].nxdata,
                                  name=entry,
                                  dims=[entry],
                                  attrs=attrs)

            # Set NXdata and NXlink attributes
            datarr.attrs["nxgroup"] = nxdata.nxname
            if isinstance(nxdata[entry], nx.NXlink):
                datarr.attrs["target"] = nxdata[entry].nxlink.nxpath

            # Add signal datarr to coords list
            coords.append(datarr)

        # ENTRY is *not* the default signal nor is listed as an axes
        else:
            # Check if there is an ENTRY_indices attribute
            # indicating the ENTRY is an axes
            index_attr = (entry+"_indices")

            if index_attr in nxdata.attrs.keys():
                # The ENTRY is indeed an axis
                index = nxdata.attrs[index_attr]
                try:
                    # Retrieve dimension name
                    dim_name = axes[index]

                    attrs = _get_attrs(nxdata[entry])
                    datarr = xr.DataArray(nxdata[entry].nxdata,
                                          name=entry,
                                          dims=[dim_name],
                                          attrs=attrs)

                    # Set NXdata and NXlink attributes
                    datarr.attrs["nxgroup"] = nxdata.nxname
                    if isinstance(nxdata[entry], nx.NXlink):
                        datarr.attrs["target"] = nxdata[entry].nxlink.nxpath

                    # Add signal datarr to coords list
                    coords.append(datarr)

                except:
                    # Axes attribute does not provide enough entries
                    # to match the ENTRY_indices attribute.
                    pass

            # If the ENTRY has the same shape as signal
            # assume it is a data variable
            elif signal_data.shape == nxdata[entry].shape:
                # Collect NXdata and NXsignal attributes
                attrs = _get_attrs(nxdata[entry])
                datarr = xr.DataArray(nxdata[entry].nxdata,
                                      name=entry,
                                      dims=axes,
                                      attrs=attrs)

                # Set NXdata and NXlink attributes
                datarr.attrs["nxgroup"] = nxdata.nxname
                if isinstance(nxdata[entry], nx.NXlink):
                    datarr.attrs["target"] = nxdata[entry].nxlink.nxpath

                # Add signal datarr to data_vars list
                data_vars.append(datarr)

            # The ENTRY can not be recognised as data variable nor
            # coordinate. This field is skipped.
            else:
                print("Warning: skipping field '{}' in '{}' group.".format(entry, nxdata.nxname))

    return data_vars, coords

def to_datset(nxentry):
    ''' Convert NeXus NXentry to an xarray Dataset
    
    This function convert the NXdata groups in the NXentry
    to DataArrays of an xarray Dataset.
    Other groups in the NXentry are saved in the Dataset attribute "NXtree" as a dictionary.
    
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

    ## Add NXentry attributes to the Dataset
    ds.attrs = _get_attrs(nxentry)

    ## Add NeXus objects to the Dataset
    NXobjects = dict()
    for nxname, nxobject in nxentry.entries.items():
        if isinstance(nxobject, nx.NXdata):
            # Add NXdata fields as data_vars and coords
            data_vars, coords = _to_datarrs(nxobject)
            for data_var in data_vars:
                ds[data_var.name] = data_var
            for coord in coords:
                ds.coords[coord.name] = coord
            # Initialize an empty placeholder NXdata with attributes
            NXobjects[nxname] = nx.NXdata(name=nxobject.nxname, attrs=nxobject.attrs)
        else:
            # Retrieve other NeXus groups in a dictionary
            NXobjects[nxname] = nxobject
    ds.attrs["NXtree"] = NXtree(NXobjects)

    # Add NXentry name attribute
    ds.attrs["NXtree"]._nxentry_name = nxentry.nxname

    return ds

def _get_attrs(nxfield):
    ''' Convert dictionary of NXattr to a common dictionary
    '''

    # Initialize attributes dictionary
    attrs = {}

    # Loop over NXattr dictionary
    # skipping some attributes specific to NXfield
    for k,v in nxfield.attrs.items():
        attrs[k] = v.nxvalue
        '''
        try:
            axes_indices = list("{}_indices".format(a) for a in nxfield.nxaxes)
        except TypeError:
            axes_indices = list()
        if k not in ["signal", "axes", "default"] + axes_indices:
            attrs[k] = v.nxvalue
        '''

    return attrs

def load(filename, entry=None):
    ''' Load a NeXus file to an xarray Dataset
    
    This function load the NXdata groups in the given NXentry
    of the NeXus file and return them as an xarray Dataset.
    Other groups in the NXentry tree are saved in the Dataset attribute "NXtree".
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

class NXtree():

    def  __init__(self, d):
        self.__dict__ = d
        self._nxentry_name = None
    
    def __str__(self):
        # Number of items (does not account "_nxentry_name" item)
        items = len(self.__dict__)-1
        return "NeXus tree ({} objects).".format(items)

    def __repr__(self):
        tree = list()
        for k, v in self.__dict__.items():
            if isinstance(v, nx.NXobject):
                tree.append(v.tree)
        return "\n".join(tree)

