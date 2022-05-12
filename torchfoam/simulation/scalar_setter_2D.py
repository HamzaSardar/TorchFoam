from typing import NoReturn

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

from torchfoam.simulation.base_parameter_setter import BaseParameterSetter


class ScalarSetter2D(BaseParameterSetter):

    def __init__(self,
                 scalar_file_path: str,
                 internal_scalar_val: float,
                 inlet_scalar_val: float):

        """
        ScalarSetter:
         - sets the internal scalar field to a given intital value.
         - currently configured for 2D.

        Parameters
        ----------
        scalar_file_path: str
            File path to '0/{scalar}', intial scalar field file.
        internal_scalar_val: float
            Value to set the internal scalar field.
        inlet_scalar_val: float
            Value to set the inlet scalar values.
        """

        self.scalar_file_path = scalar_file_path
        self.internal_scalar_val = internal_scalar_val
        self.inlet_scalar_val = inlet_scalar_val

    def set_parameter(self) -> NoReturn:

        """Function to parse parameter file as dictionary and set values.
        """
        scalar = ParsedParameterFile(self.scalar_file_path)

        scalar['internalField'] = 'uniform', [self.internal_scalar_val]
        scalar['boundaryField']['leftInlet']['value'] = 'uniform', [self.inlet_scalar_val]

        scalar.writeFile()
