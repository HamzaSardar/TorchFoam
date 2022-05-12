from typing import NoReturn
from pathlib import Path

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

from torchfoam.simulation.base_parameter_setter import BaseParameterSetter


class DiffusionSetter(BaseParameterSetter):

    def __init__(self,
                 case_dir: Path,
                 diffusion_constant: float):

        """
        ScalarSetter:
         - sets the internal scalar field to a given intital value.
         - currently configured for 2D.

        Parameters
        ----------
        case_dir: Path
            File path to case.
        diffusion_constant: float
            Value to set the diffusion constant.
        inlet_scalar_val: float
            Value to set the inlet scalar values.
        """

        self.file_path = case_dir / 'constant/transportProperties'
        self.diffusion_constant = diffusion_constant

    def set_parameter(self) -> NoReturn:

        """Function to parse parameter file as dictionary and set values.
        """
        diffusion = ParsedParameterFile(str(self.file_path))
        diffusion['DT'] = 'DT', '[0 2 -1 0 0 0 0]', self.diffusion_constant

        diffusion.writeFile()
