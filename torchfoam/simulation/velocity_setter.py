import math
import random

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


class VelocitySetter:

    def __init__(self, u_file_path, min_theta=float(10), max_theta=float(80)):

        """
        VelocitySetter:
         - sets the internal velocity field to a random vector.
         - currently configured for 2D.

        Parameters
        ----------
        u_file_path: str
            File path to '0/U', intial velocity field file.
        min_theta: float
            Lower bound for angle of velocity vector to the +x axis.
        max_theta: float
            Upper bound for angle of velocity vector to the +x axis.
        """

        self.u_file_path = u_file_path
        self.min_theta = min_theta
        self.max_theta = max_theta
        self.vel_vector = self._vel_generator_uniform(10, 80)
        self.ux = self.vel_vector[0]
        self.uy = self.vel_vector[1]
        self.theta = self.vel_vector[2]

    def set_velocity(self):

        """Function to parse parameter file as dictionary and set values.
        """
        vel = ParsedParameterFile(self.u_file_path)

        vel['internalField'] = 'uniform', [self.ux, self.uy, 0]
        vel['boundaryField']['leftInlet']['value'] = 'uniform', [self.ux, self.uy, 0]

        vel.writeFile()

    @staticmethod
    def _vel_generator_uniform(min_theta, max_theta):

        """Helper method to generate velocity vector.

        Parameters
        ----------
        min_theta: float
            Lower bound for angle of velocity vector to the +x axis.
        max_theta: float
            Upper bound for angle of velocity vector to the +x axis.

        Returns
        -------
        ux: float
            x-component of velocity.
        uy: float
            y-component of velocity.
        theta: float
            Angle between velocity and +x axis.
        """

        theta = random.uniform(min_theta, max_theta)
        ux = math.cos(math.radians(theta))
        uy = math.sin(math.radians(theta))

        return [ux, uy, theta]
