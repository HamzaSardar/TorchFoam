import numpy as np

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


class CreateTensor:
    def __init__(self,
                 require_u=True,
                 u_dir=None):
        self.require_u = require_u
        self.u_dir = u_dir
        if require_u and u_dir is None:
            raise ValueError('If U values required in tensor, please provide case/0/U')

    def __call__(self, *args, **kwargs):
        return self.return_np_tensor(*args)

    def return_np_tensor(self, *np_arrays):
        if self.require_u:
            u_tensor = self._create_u_tensor(self.u_dir, int(len(np_arrays[0])))
            np_temp =  np.concatenate((np_arrays), axis=1)
            return np.concatenate((np_temp, u_tensor), axis=1)
        else:
            return np.concatenate((np_arrays), axis=1)

    @staticmethod
    def _create_u_tensor(u_dir, num_rows):
        u = ParsedParameterFile(u_dir)
        u_x = float(u['internalField']['uniform'][0])
        u_y = float(u['internalField']['uniform'][1])
        u_z = float(u['internalField']['uniform'][2])

        u_tensor = np.zeros((num_rows, 3))

        u_tensor[:, 0] += u_x
        u_tensor[:, 1] += u_y
        u_tensor[:, 2] += u_z
        return u_tensor
