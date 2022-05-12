from pathlib import Path

from PyFoam.Execution.BasicRunner import BasicRunner

import torchfoam.simulation.velocity_setter_2D as velocity_setter_2D
import torchfoam.simulation.diffusion_setter as diffusion_setter


class Solver:

    def __init__(self, case_dir: Path, mode:str, **kwargs) -> None:

        """
        Solver:
         - sets parameters and runs simulation.
         - Currently configured to run scalarTransportFoam.

        Parameters
        ----------
        case_dir: Path
            Directory for OpenFoam case as complete path.
        mode: str
            Training or Evaluation.
        fixed_theta : Union[float, None]
            If a set value of theta is required, it may be set in **kwargs.
        """

        self.mode = mode
        self.case_dir = case_dir
        for key in kwargs.keys():
            if key in ['theta', 'fixed_theta']:
                self.fixed_theta = float(kwargs[key])
            if key in ['alpha', 'DT']:
                self.alpha = float(kwargs[key])

    def run_solver(self) -> None:

        """Instatiates and runs velocity setter, followed by solver.
        """
        global v
        global d

        if self.fixed_theta:
            v = velocity_setter_2D.VelocitySetter2D(self.case_dir / '0/U', fixed_theta=float(self.fixed_theta),
                                                    mode=self.mode)
            print(v.fixed_theta)
        if self.alpha:
            d = diffusion_setter.DiffusionSetter(self.case_dir, diffusion_constant=float(self.alpha))
        else:
            v = velocity_setter_2D.VelocitySetter2D(self.case_dir / '0/U', mode=self.mode)
            d = diffusion_setter.DiffusionSetter(self.case_dir, diffusion_constant=0)

        v.set_parameter()
        d.set_parameter()

        BasicRunner(argv=['scalarTransportFoam', '-case', str(self.case_dir)]).start()
