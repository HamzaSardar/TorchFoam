from PyFoam.Execution.BasicRunner import BasicRunner
import simulation.velocity_setter


class Solver:

    def __init__(self, case_dir):
        self.case_dir = case_dir

    def run_solver(self):
        v = simulation.velocity_setter.VelocitySetter(self.case_dir + '/0/U')
        v.set_velocity()

        BasicRunner(argv=['scalarTransportFoam', '-case', self.case_dir]).start()
