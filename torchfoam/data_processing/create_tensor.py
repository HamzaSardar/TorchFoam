from typing import Union

import numpy as np
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


class CreateTensor:
    def __init__(self,
                 require_u: bool = True,
                 require_cell_Re: bool = True,
                 u_dir: Union[None, str] = None,
                 vol_tensor: np.array = None,
                 nu: float = None) -> None:


        """
        CreateTensor:
         - Pass in numpy tensors and concatenate into one tensor.
         - Creates a tensor of U values for a uniform U field, and concatenates.
         - Creates a tensor of local (cell) Re values, based on cube root cell volume.
         - Returns a tensor of (n samples) x (m columns)

        Parameters
        ----------
        require_u: bool
            Is a tensor of U values required?
        require_cell_Re: bool
            Is a tensor of local (cell) Re required?
        u_dir: str
            Path to velocity results file.
        vol_tensor: np.array
            Numpy array of cell volumes.
        nu: float
            Kinematic viscosity.
        """

        self.require_u = require_u
        self.require_cell_Re = require_cell_Re
        self.u_dir = u_dir
        self.vol_tensor = vol_tensor
        self.nu = nu

        if require_u and u_dir is None:
            raise ValueError('If U values required in tensor, please provide case/0/U')
        if require_cell_Re and u_dir is None:
            raise ValueError('Cell Re cannot be calculated without U values. Please provide case/0/U')
        if require_cell_Re and vol_tensor is None:
            raise ValueError('Cell Re cannot be calculated without cell volumes.' + '\n' +
                             'Please provide Numpy array of cell volumes.')

    def __call__(self, *args, **kwargs) -> np.array:
        return self.return_np_tensor(*args)

    def return_np_tensor(self, *np_arrays) -> np.array:

        """Returns a single tensor containing data from simulation.

        Parameters
        ----------
        np_arrays: *numpy.array
            Variable number of numpy arrays depending on data to include in final tensor.

        Returns
        -------
        np.array
            Single numpy tensor containing all data required.
        """

        if self.require_u:
            u_tensor = self._create_u_tensor(self.u_dir, int(len(np_arrays[0])))
            np_temp =  np.concatenate((np_arrays), axis=1)
            np_temp = np.concatenate((np_temp, u_tensor), axis=1)
            if self.require_cell_Re:
                Re_tensor = self._create_Re_tensor(u_tensor)
                np.temp = np.concatenate((np_temp, Re_tensor), axis =1)
        else:
            np_temp = np.concatenate((np_arrays), axis=1)

        return np_temp

    @staticmethod
    def _create_u_tensor(u_dir: str, num_rows: int) -> np.array:

        """Helper function to create a tensor of velocity values at each cell for a uniform field.

        Parameters
        ----------
        u_dir: str
            File path to velocity results field.
        num_rows: int
            Number of rows required in velocity tensor.

        Returns
        -------
        u_tensor: np.array
            Tensor of x, y, z, components of velocity.
        """

        u = ParsedParameterFile(u_dir)
        u_x = float(u['internalField']['uniform'][0])
        u_y = float(u['internalField']['uniform'][1])
        u_z = float(u['internalField']['uniform'][2])

        u_tensor = np.zeros((num_rows, 3))

        u_tensor[:, 0] += u_x
        u_tensor[:, 1] += u_y
        u_tensor[:, 2] += u_z
        return u_tensor

    def _create_Re_tensor(self, u_tensor: np.array) -> np.array:
        return (np.divide(np.multiply(u_tensor, np.cbrt(self.vol_tensor)), self.nu))