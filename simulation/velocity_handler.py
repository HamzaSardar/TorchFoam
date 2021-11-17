import random
import math

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


class VelocityHandler:

    def __init__(self, u_file_path, min_theta, max_theta):
        self.u_file_path = u_file_path
        self.min_theta = min_theta
        self.max_theta = max_theta
        self.vel_vector = self._vel_generator_uniform(10, 80)
        self.ux = self.vel_vector[0]
        self.uy = self.vel_vector[1]
        self.theta = self.vel_vector[2]

    def set_velocity(self):
        vel = ParsedParameterFile(self.u_file_path)

        vel['internalField'] = 'uniform', [self.ux, self.uy, 0]
        vel['boundaryField']['leftInlet']['value'] = 'uniform', [self.ux, self.uy, 0]

        vel.writeFile()

    @staticmethod
    def _vel_generator_uniform(min_theta, max_theta):
        theta = random.uniform(min_theta, max_theta)
        ux = math.cos(math.radians(theta))
        uy = math.sin(math.radians(theta))

        return [ux, uy, theta]
