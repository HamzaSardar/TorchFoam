from PyFoam.Execution.BasicRunner import BasicRunner
import simulation.velocity_handler
import shutil


class RunSolver:

    def __init__(self, case_dir, dst_dir):
        self.case_dir = case_dir
        self.dst_dir = dst_dir

    def solver(self):
        v = simulation.velocity_handler.VelocityHandler(self.case_dir + '/0/U')
        v.set_velocity()

        BasicRunner(argv=['scalarTransportFoam', '-case', self.case_dir]).start()

        #self._copy_data(self.case_dir + '/postProcessing/singleGraph/9.5/line_T.csv', self.dst_dir + '_theta_' + str(v.theta))

    @staticmethod
    def _copy_data(src_dir, dst_dir):
        shutil.copy(src_dir, dst_dir)
