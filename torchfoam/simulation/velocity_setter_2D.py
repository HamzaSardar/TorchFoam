import math
import random
from typing import NoReturn, Union, List

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

from torchfoam.simulation.base_parameter_setter import BaseParameterSetter


class VelocitySetter2D(BaseParameterSetter):

    def __init__(self,
                 u_file_path: str,
                 min_theta: int = int(10),
                 max_theta: int = int(80),
                 fixed_theta: Union[float, None] = None) -> None:

        """
        VelocitySetter:
         - sets the internal velocity field to a random vector.
         - currently configured for 2D.

        Parameters
        ----------
        u_file_path: str
            File path to '0/U', intial velocity field file.
        min_theta: int
            Lower bound for angle of velocity vector to the +x axis.
        max_theta: int
            Upper bound for angle of velocity vector to the +x axis.
        """

        self.u_file_path = u_file_path
        self.min_theta = min_theta
        self.max_theta = max_theta
        self.fixed_theta = fixed_theta
        self.vel_vector = self._get_parameter()
        self.ux = self.vel_vector[0]
        self.uy = self.vel_vector[1]
        self.theta = self.vel_vector[2]

    def set_parameter(self) -> NoReturn:

        """Function to parse parameter file as dictionary and set values.
        """
        vel = ParsedParameterFile(self.u_file_path)

        vel['internalField'] = 'uniform', [self.ux, self.uy, 0]
        vel['boundaryField']['leftInlet']['value'] = 'uniform', [self.ux, self.uy, 0]

        vel.writeFile()

    def _get_parameter(self) -> Union[float, List[float]]:

        """Helper method to generate parameter. Here a random velocity vector is generated.

        Returns
        -------
        ux: float
            x-component of velocity.
        uy: float
            y-component of velocity.
        theta: float
            Angle between velocity and +x axis.
        """
        if not self.fixed_theta:
            theta = random.uniform(self.min_theta, self.max_theta)
            ux = math.cos(math.radians(theta))
            uy = math.sin(math.radians(theta))
        else:
            theta = self.fixed_theta
            ux = math.cos(math.radians(theta))
            uy = math.sin(math.radians(theta))

        return [ux, uy, theta]
