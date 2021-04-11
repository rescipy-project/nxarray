import nexusformat.nexus as nx
import xarray as xr

@xr.register_dataarray_accessor("nxr")
class _nxrDataArray:
    '''nxarray class extending xarray DataArray
    '''

    def __init__(self, xarray_dataarray):
        self._datarr = xarray_dataarray

        #self._nxgroup = None
        #self._nxgroup_attrs = None

@xr.register_dataset_accessor("nxr")
class _nxrDataset:
    '''nxarray class extending xarray Dataset
    '''

    def __init__(self, xarray_dataset):
        self._datset = xarray_dataset

        self._NXentry_name = None

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
        if self._NXentry_name:
            nxentry_name = self._NXentry_name
        else:
            nxentry_name = "entry"
        nxentry = nx.NXentry(name=nxentry_name)

        ## Add dataset attributes to NXentry
        _add_attrs(self._datset.attrs, nxentry)

        # Add any other NeXus group to the dataset
        for nxname, nxobject in self._datset.attrs["NX"].__dict__.items():
            nxentry[nxname] = nxobject

        ## Add DataArrays as NXdata groups
        self._add_nxdata(nxentry)

        return nxentry

    def _add_nxdata(self, nxentry):

        ## Cycle over data variables and coordinates
        for variable in self._datset.variables:

            datarr = self._datset[variable]

            ## Create NXdata group if not present
            if "nxgroup" in datarr.attrs:
                nxdata_name = datarr.attrs["nxgroup"]
            else:
                nxdata_name = "data"
            if nxdata_name not in nxentry:
                nxentry[nxdata_name] = nx.NXdata()
            # Add NXdata attributes
            if "nxgroup_attrs" in datarr.attrs:
                _add_attrs(datarr.attrs["nxgroup_attrs"], nxentry[nxdata_name])
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

        ## Add @axes, @signal and @AXIS_indices to NXdata if not present
        if "axes" not in nxentry[nxdata_name].attrs:
            nxentry[nxdata_name].attrs["axes"] = list(self._datset.dims)
        if "signal" not in nxentry[nxdata_name].attrs:
            nxentry[nxdata_name].attrs["signal"] = list(self._datset.data_vars)[0]
        for coord in self._datset.coords.keys():
            if (coord+"_indices") not in nxentry[nxdata_name].attrs:
                for index, dim in enumerate(self._datset.dims):
                    if self._datset[coord].dims[0] == dim:
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

def _add_attrs(attrs, nxfield):
    for k,v in attrs.items():
        if k not in ["NX", "nxgroup", "nxgroup_attrs"]:
            nxfield.attrs[k] = v
