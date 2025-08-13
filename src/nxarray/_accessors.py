import nexusformat.nexus as nx
import xarray as xr

@xr.register_dataarray_accessor("nxr")
class _nxrDataArray:
    '''nxarray class extending xarray DataArray
    '''

    def __init__(self, xarray_dataarray):
        self._da = xarray_dataarray

@xr.register_dataset_accessor("nxr")
class _nxrDataset:
    '''nxarray class extending xarray Dataset
    '''

    def __init__(self, xarray_dataset):
        self._ds = xarray_dataset

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
        if "NXtree" in self._ds.attrs:
            nxentry_name = self._ds.attrs["NXtree"]._nxentry_name
        else:
            nxentry_name = "entry"
        nxentry = nx.NXentry(name=nxentry_name)

        ## Add dataset attributes to NXentry
        _add_attrs(self._ds.attrs, nxentry)

        # Add NeXus groups to the dataset
        # (to be done before adding DataArrays in order
        # to properly initialize NXdata groups)
        if "NXtree" in self._ds.attrs:
            for nxname, nxobject in self._ds.attrs["NXtree"].__dict__.items():
                if isinstance(nxobject, nx.NXobject):
                    nxentry[nxname] = nxobject

        ## Add DataArrays in NXdata groups
        self._add_nxdata(nxentry)

        return nxentry

    def _add_nxdata(self, nxentry):

        ## Cycle over data variables and coordinates
        if self._ds.variables:
            for variable in self._ds.variables:

                datarr = self._ds[variable]

                ## Create NXdata group if not present
                if "nxgroup" in datarr.attrs:
                    nxdata_name = datarr.attrs["nxgroup"]
                else:
                    nxdata_name = "data"
                if nxdata_name not in nxentry:
                    nxentry[nxdata_name] = nx.NXdata()
                # Get field path
                nxfield_path = nxdata_name + "/" + datarr.name

                if "target" in datarr.attrs:
                    # The field is an NXlink
                    target = datarr.attrs['target']
                    nxentry[nxfield_path] = nx.NXlink(target, name=datarr.name, abspath=True)
                else:
                    nxentry[nxfield_path] = nx.NXfield(datarr.values, name=datarr.name)

                # Add attributes to the field
                _add_attrs(datarr.attrs, nxentry[nxfield_path])

            ## Add @axes attribute to NXdata if not present
            if "axes" not in nxentry[nxdata_name].attrs:
                nxentry[nxdata_name].attrs["axes"] = list(self._ds.dims)

            ## Add @signal attribute to NXdata if not present
            if "signal" not in nxentry[nxdata_name].attrs:
                signal = ""
                # Look for @signal attribute in data variables
                for data_var in list(self._ds.data_vars):
                    if "signal" in self._ds[data_var].attrs:
                        signal = data_var
                if signal == "":
                    # No @signal attributes found.
                    # Pick first data variable as signal
                    signal = list(self._ds.data_vars)[0]
                nxentry[nxdata_name].attrs["signal"] = signal

        ## Add @AXIS_indices attributes to NXdata if not present
        if self._ds.coords.keys():
            for coord in self._ds.coords.keys():
                if (coord+"_indices") not in nxentry[nxdata_name].attrs:
                    for index, dim in enumerate(self._ds.dims):
                        if self._ds[coord].dims[0] == dim:
                            nxentry[nxdata_name].attrs[coord+"_indices"] = index

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
        nxentry = self.to_nxentry()

        ## Save to file
        nxentry.save(filename, **kwargs)

@xr.register_datatree_accessor("nxr")
class _nxrDataTree:
    '''nxarray class extending xarray DataTree
    '''

    def __init__(self, xarray_datatree):
        self._dt = xarray_datatree

def _add_attrs(attrs, nxfield):
    for k,v in attrs.items():
        if k not in ["NXtree", "nxgroup"]:
            nxfield.attrs[k] = v
