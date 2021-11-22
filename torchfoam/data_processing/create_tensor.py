import numpy as np

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


class CreateTensor:
    def __init__(self,
                 require_u=True,
                 u_dir=None):

        """
        CreateTensor:
         - Pass in numpy tensors and concatenate into one tensor.
         - Creates a tensor of U values for a uniform U field, and concatenates.
         - Returns a tensor of (n samples) x (m columns)

        Parameters
        ----------
        require_u: bool
            Is a tensor of U values required?
        u_dir: str
            Path to velocity results file.
        """

        self.require_u = require_u
        self.u_dir = u_dir
        if require_u and u_dir is None:
            raise ValueError('If U values required in tensor, please provide case/0/U')

    def __call__(self, *args, **kwargs):
        return self.return_np_tensor(*args)

    def return_np_tensor(self, *np_arrays):

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
            return np.concatenate((np_temp, u_tensor), axis=1)
        else:
            return np.concatenate((np_arrays), axis=1)

    @staticmethod
    def _create_u_tensor(u_dir, num_rows):

        """Helper function to create a tensor of velocity values at each cell for a uniform field.

        Parameters
        ----------
        u_dir:
            File path to velocity results field.
        num_rows:
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
