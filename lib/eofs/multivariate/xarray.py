

import xarray as xr

from eofs import xarray




class MultivariateEOF:
    '''Multivariate Empirical Orthoganal Functions for xarray format'''


    def __init__(self, datasets, weights=None,center=True, ddof=1):
        '''

        Inputs:

        *Datasets*
            Takes in a list of xarray DataArrays. The first dimension of the array
            must represent a time series.

        *weights*
            Currently does not hold functionality. In the future, would be used to
            weight the input datasets.

        *center*
            Currently does not hold functionality. In the future, would be used to
            determine whether or not the time-mean is removed from the data. True is
            default as most of the time looking at variance from the mean is most useful

        *ddof*
            Currently does not hold functionality. In the future, this would be used to
            set the degrees of freedom.


        Returns and Important Information:

        *solver*
            The _solver calls the Eof class from xarray.py for single variables and
            sets it for the multivariate EOF object.

            
        *data, info*
            The data and info will be stored using the _merge_fields. This contains
            information regarding the shapes/slicing of variable arrays.

        
        '''
        self._ndata = len(datasets)

        # Define data and info from the merge fields function
        data, info = self._merge_fields(datasets)
        self._shapes = info['shapes']
        self._slicers = info['slicers']

        # The solver will be from xarray.py for single variable and accept input of data
        self._solver = xarray.Eof(data)

        self.neofs = self._solver.neofs


    def _merge_fields(self, fields):
        '''
        Merge fields is responsible for flattening the input variable arrays into a
        (time, space) format. This is done by reorganizing the field dimensions using
        .stack creating a new dimension 'space'. The first dimension (time) is left
        alone. Time dimensions among the input fields must be identical. After
        flattening, the fields are then concatenated along the new 'space' dimension.

        Inputs:

        *fields*
            Fields is the variable fields that need to be merged before analysis. They
            should be formatted as a list of xarray DataArrays.

        Returns:

        *merged*
            Merged is the (time,space) field returned as an xarray DataArray after
            combining the input variable fields.

        *info*
            Info is a dictionary that contains the shapes and slicers information
            regarding how the input fields were concatenated. Variable 1 will come first
            in the list for shapes and slicers respectively. Field #1 slice will go
            from 0 to channels (the product of the non-time dimensions). Field 2 slice
            will go from there plus channels for field 2.
        
        '''

        # Def info dictionary to fill with shape and slice info
        info = {'shapes': [], 'slicers': []}
        islice = 0
        

        # Make storage list for (time,space) fields
        flattened_fields = []


        # For each variable field
        for field in fields:

            info['shapes'].append(field.shape[1:]) # Add shapes to list. No time dim


            # Calculate channels (expansion of field when flat)
            # Product of non-time dimension shapes
            channels = 1
            for i in range(len(field.dims) - 1):
                  channels = channels * field.shape[i+1] 


            # Store info on where the slices were taken and update slice value each loop
            info['slicers'].append(slice(islice, islice+channels)) # slice(Start, Stop)
            islice += channels # Updates islice

            # Help reorganize the field. These are the dims to be combined
            stacking_dimensions = [ dim for dim in field.dims if dim != field.dims[0] ]

            # Stack them over new dim "space". Typically lat,lon. Result (time,space)
            flat_field = field.stack( space = (stacking_dimensions) )

            # Add field to fields list to concat
            flattened_fields.append(flat_field)


        try:
            # Merge the fields together
            merged = xr.concat( flattened_fields, dim = 'space')

        
        except ValueError: # For when the time dims don't match. Required for function.
            raise ValueError("All fields must have the same first dimension (time)")


        return merged, info



    def _unwrap(self, modes):
        '''
        _unwrap does not currently hold functionality. It would be used to seperate
        variables before calculating the eofs.
        
        
        '''
        nmodes = modes.shape[0]
        # modeset = 
        # return modeset
    

    def eofs(self, eofscaling=0, neofs=None):
        '''
        Due to currently unfunctional _unwrap, eofs does not hold functionality.

        eofs woulld be responsible for calculating the Empirical Orthogonal Functions
        (EOFs) as an ordered xarray DataArray.

        eofs calls the modes determined by __init__ solver to calculate the associated
        EOFs
        
        
        '''

        modes = self._solver.eofs(eofscaling, neofs)
        return self._unwrap(modes)



    def eigenvalues(self, neighs=None):
        '''
        Eigenvalues is responsible for calculating the eigenvalues corresponding to the
        EOF modes. The order will be from greatest variance to smallest variance.

        Returns:

        *eigenvalues*
            eigenvalues will return as an xarray DataArray calculated from the solver
            set by __init__
        
        '''

        return self._solver.eigenvalues()

