from PyFoam.Execution.BasicRunner import BasicRunner

import torchfoam.simulation.velocity_setter_2D as velocity_setter_2D


class Solver:

    def __init__(self, case_dir: str, **kwargs) -> None:

        """
        Solver:
         - sets parameters and runs simulation.
         - Currently configured to run scalarTransportFoam.

        Parameters
        ----------
        case_dir: str
            Directory for OpenFoam case as complete path.
        fixed_theta : Union[float, None]
            If a set value of theta is required, it may be set in **kwargs.
        """
        self.case_dir = case_dir
        for key in kwargs.keys():
            if key in ['theta', 'fixed_theta']:
                self.fixed_theta = float(kwargs[key])

    def run_solver(self) -> None:

        """Instatiates and runs velocity setter, followed by solver.
        """
        if self.fixed_theta:
            v = velocity_setter_2D.VelocitySetter2D(self.case_dir + '/0/U', fixed_theta=float(self.fixed_theta))
            print(v.fixed_theta)
        else:
            v = velocity_setter_2D.VelocitySetter2D(self.case_dir + '/0/U')

        v.set_parameter()

        BasicRunner(argv=['scalarTransportFoam', '-case', self.case_dir]).start()
