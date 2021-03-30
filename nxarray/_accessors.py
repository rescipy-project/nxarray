import nexusformat.nexus as nx
import xarray as xr

@xr.register_dataarray_accessor("nxr")
class _nxrDataArray:
    '''nxarray class extending xarray DataArray
    '''

    def __init__(self, xarray_dataarray):
        self._datarr = xarray_dataarray

    def to_nxdata(self):
        ''' Convert xarray DataArray to NeXus NXdata
        
        Returns:
            NeXus NXdata
        
        Example:
            import nxarray as nxr
            
            dr = xarray.DataArray()
            nxdata = dr.nxr.to_nxdata()
        '''

        ## Initialize NXdata
        nxname = self._datarr.name if self._datarr.name != None else "data"
        nxdata = nx.NXdata(name=nxname)

        ## Add dataset to NXdata
        self._add_to(nxdata)

        return nxdata

    def _add_to(self, nxdata):
        ''' Add DataArray to NXdata as signal with axes
        '''

        ## Add signal
        self._add_signal(nxdata)

        ## Add axes
        self._add_axes(nxdata)

        ## Add DataArray attributes to signal
        _add_attrs(self._datarr.attrs, nxdata.nxsignal)

    def _add_signal(self, nxdata):
        signal_name = self._datarr.name if self._datarr.name != None else "signal"
        nxdata.nxsignal = nx.NXfield(self._datarr.values, name=signal_name)
    
    def _add_axes(self, nxdata):
        for coord_name in self._datarr.coords:
            axes = self._datarr.coords[coord_name].values
            nxdata.nxaxes = nx.NXfield(axes, name=coord_name)
        # Overwrite the list of all xarray coordinates with just xarray dimensions
        nxdata.attrs["axes"] = list(self._datarr.dims)

    def save(self, filename, **kwargs):
        ''' Save xarray DataArray to NeXus file
        
        Arguments:
            filename: file path to .nx file
            **kwargs: any optional argument accepted by NXdata.save() method
        
        Returns:
            nothing
        
        Example:
            import nxarray as nxr
            
            dr = xarray.DataArray()
            dr.nxr.save(path/to/file.nx)
        '''

        ## Initialize NXdata
        nxdata = self._datarr.nxr.to_nxdata()

        ## Save to file
        nxdata.save(filename, **kwargs)

@xr.register_dataset_accessor("nxr")
class _nxrDataset:
    '''nxarray class extending xarray Dataset
    '''

    def __init__(self, xarray_dataset):
        self._datset = xarray_dataset

    def to_nxentry(self):
        ''' Convert xarray Dataset to NeXus NXentry
        
        Returns:
            NeXus NXentry
        
        Example:
            import nxarray as nxr
            
            ds = xarray.Dataset()
            nxentry = ds.nxr.to_nxentry()
        '''

        ## Initialize NXentry
        nxentry = nx.NXentry()

        for name, datarr in self._datset.data_vars.items():
            nxentry[name] = datarr.nxr.to_nxdata()

        ## Add dataset attributes to NXentry
        _add_attrs(self._datset.attrs, nxentry)

        # Add any other NeXus groups to the dataset
        try:
            for nxname, nxobject in self._datset.attrs["NX"].items():
                nxentry[nxname] = nxobject
        except KeyError:
            pass

        return nxentry

    def save(self, filename, **kwargs):
        ''' Save xarray Dataset to NeXus file
        
        Arguments:
            filename: file path to .nx file
            **kwargs: any optional argument accepted by NXentry.save() method
        
        Returns:
            nothing
        
        Example:
            import nxarray as nxr
            
            ds = xarray.Dataset()
            ds.nxr.save(path/to/file.nx)
        '''

        ## Initialize NXentry
        nxentry = self._datset.nxr.to_nxentry()

        ## Save to file
        nxentry.save(filename, **kwargs)

def _add_attrs(attrs, nxfield):
    for k,v in attrs.items():
        # Avoid any overwriting of specific NXfield attributes
        try:
            axes_indices = list("{}_indices".format(a) for a in nxfield.nxaxes)
        except TypeError:
            axes_indices = list()
        if k not in ["signal", "axes", "default", "NX"] + axes_indices:
            nxfield.attrs[k] = v
