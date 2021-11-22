from PyFoam.Execution.BasicRunner import BasicRunner

import torchfoam.simulation.velocity_setter_2D as velocity_setter_2D


class Solver:

    def __init__(self, case_dir: str) -> None:

        """
        Solver:
         - sets parameters and runs simulation.
         - Currently configured to run scalarTransportFoam.

        Parameters
        ----------
        case_dir: str
            Directory for OpenFoam case as complete path.
        """
        self.case_dir = case_dir

    def run_solver(self) -> None:

        """Instatiates and runs velocity setter, followed by solver.
        """

        v = velocity_setter_2D.VelocitySetter2D(self.case_dir + '/0/U')
        v.set_parameter()

        BasicRunner(argv=['scalarTransportFoam', '-case', self.case_dir]).start()
