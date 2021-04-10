import nexusformat.nexus as nx
import xarray as xr

@xr.register_dataarray_accessor("nxr")
class _nxrDataArray:
    '''nxarray class extending xarray DataArray
    '''

    def __init__(self, xarray_dataarray):
        self._datarr = xarray_dataarray

        #self._NXdata_name = None
        #self._NXdata_attrs = None

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

            ## Create NXdata group if not present and add attributes to it
            if "NXdata_name" in datarr.attrs:
                nxdata_name = datarr.attrs["NXdata_name"]
                if nxdata_name not in nxentry:
                    nxentry[nxdata_name] = nx.NXdata()
                if "NXdata_attrs" in datarr.attrs:
                    _add_attrs(datarr.attrs["NXdata_attrs"], nxentry[nxdata_name])
                # Get field path
                nxfield_path = nxdata_name + "/" + datarr.name
            else:
                nxfield_path = datarr.name

            if "target" in datarr.attrs:
                # The field is an NXlink
                target = datarr.attrs['target']
                nxentry[nxfield_path] = nx.NXlink(target, name=datarr.name, abspath=True)
            else:
                nxentry[nxfield_path] = nx.NXfield(datarr.values, name=datarr.name)

            # Add attributes to the field
            _add_attrs(datarr.attrs, nxentry[nxfield_path])

            #TODO Add @axes, @signal and @AXIS_indices of not present

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
        if k not in ["NX", "NXdata_name", "NXdata_attrs"]:
            nxfield.attrs[k] = v
