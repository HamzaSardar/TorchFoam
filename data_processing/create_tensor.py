import numpy as np

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


class CreateTensor:
    def __init__(self,
                 require_u=True,
                 u_dir=None,
                 *np_arrays):
        self.require_u = require_u
        self.u_dir = u_dir
        self.np_arrays = np_arrays
        if require_u and u_dir is None:
            raise ValueError('If U values required in tensor, please provide case/0/U')

    def return_np_tensor(self):
        if self.require_u:
            u_tensor = self.create_u_tensor()
            return np.concatenate((self.np_arrays, u_tensor), axis=1)
        else:
            return np.concatenate((self.np_arrays), axis=1)

    def create_u_tensor(self):
        u = ParsedParameterFile(self.u_dir)
        u_x = float(u['internalField']['uniform'][0])
        u_y = float(u['internalField']['uniform'][1])
        u_z = float(u['internalField']['uniform'][2])

        u_tensor = np.zeros((len(self.np_arrays[0]), 3))

        u_tensor[:, 0] += u_x
        u_tensor[:, 1] += u_y
        u_tensor[:, 2] += u_z
        return u_tensor
