

import xarray as xr

from eofs import xarray




class MultivariateEOF:

    # For now, I will likely not use weights, center, or ddof.
    def __init__(self, datasets, weights=None,center=True, ddof=1):
 
        self._ndata = len(datasets)

        # Define data and info from the merge fields function
        data, info = self._merge_fields(datasets)
        self._shapes = info['shapes']
        self._slicers = info['slicers']

        # The solver will be from xarray.py for single variable and accept input of data
        self._solver = xarray.Eof(data)

        self.neofs = self.solver.neofs


    def _merge_fields(self, fields):
        
        # Def info dict to fill with shape and slice info
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
            #Merge the fields together
            merged = xr.concat( flattened_fields, dim = 'space')

        
        except ValueError: # For when the time dims don't match. Required for function.
            raise ValueError("All fields must have the same first dimension 'time' ")


        return merged, info



    #def eofs(self, ):



    #def eigenvalues(self, ):


