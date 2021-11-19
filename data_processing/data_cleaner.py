import numpy as np


class DataCleaner:

    def __init__(self, results_dir, mode):
        self.results_dir = results_dir
        self.mode = mode
        self.results = None
        self.np_results = None
        self.num_samples = None
        self.specials = {'\n': ' ', '(': '', ')': '', ';': ''}

    def load_data(self):
        with open(self.results_dir, 'r') as f:
            self.results = f.readlines()

    def get_samples(self):
        samples_trans_table = self.results[20].maketrans(self.specials)
        self.num_samples = np.fromstring(self.results.translate(samples_trans_table))

    def clean_data(self):
        self.results = self.results[22: 22 + self.num_samples + 1]
        self.results = ' '.join(self.results).lower()
        results_trans_table = self.results.maketrans(self.specials)
        clean_data = self.results.translate(results_trans_table)
        self.np_results = np.fromstring(clean_data, sep=' ')

    def return_data(self) -> np.array:
        if self.mode == 's':
            return self.results.reshape(self.num_samples, 1)
        if self.mode == 'v':
            return self.results.reshape(self.num_samples, 3)
