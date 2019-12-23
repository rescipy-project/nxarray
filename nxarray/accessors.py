import nexusformat.nexus as nx
import xarray as xr

@xr.register_dataarray_accessor("nxr")
class DataArray:
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
        nxdata = nx.NXdata()

        ## Add signal attribute
        signal_name = self._datarr.name if self._datarr.name != '' else 'signal'
        nxdata.nxsignal=nx.NXfield(self._datarr.values, name=signal_name)

        ## Add axes attribute
        for axes_name in self._datarr.coords:
            axes = self._datarr.coords[axes_name].values
            nxdata.nxaxes=nx.NXfield(axes, name=axes_name)
        # Overwrite the list of all xarray coordinates with just xarray dimensions
        nxdata.attrs["axes"] = list(self._datarr.dims)

        ## Add metadata
        for k,v in self._datarr.attrs.items():
            # Avoid any overwriting of specific NXdata attributes
            if k not in [signal_name, "axes"] + ["{}_indices".format(a) for a in nxdata.nxaxes]:
                nxdata.attrs[k] = v

        return nxdata

    def save(self, filename):
        ''' Save xarray DataArray to NeXus file
        
        Arguments:
            filename: file path to .nx file
        
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
        nxdata.save(filename)

@xr.register_dataset_accessor("nxr")
class Dataset:
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

        return nxentry

    def save(self, filename):
        ''' Save xarray Dataset to NeXus file
        
        Arguments:
            filename: file path to .nx file
        
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
        nxentry.save(filename)
