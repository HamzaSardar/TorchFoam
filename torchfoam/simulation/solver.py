from PyFoam.Execution.BasicRunner import BasicRunner

import torchfoam.simulation.velocity_setter as velocity_setter


class Solver:

    def __init__(self, case_dir):

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

    def run_solver(self):

        """Instatiates and runs velocity setter, followed by solver.
        """

        v = velocity_setter.VelocitySetter(self.case_dir + '/0/U')
        v.set_velocity()

        BasicRunner(argv=['scalarTransportFoam', '-case', self.case_dir]).start()
