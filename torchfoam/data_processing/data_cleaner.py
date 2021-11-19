import numpy as np


class DataCleaner:

    def __init__(self, mode):
        self.mode = mode
        self.results = None
        self.specials = {'\n': ' ', '(': '', ')': '', ';': ''}

    def __call__(self, *args, **kwargs):
        return self.get(*args)

    def get(self, results_dir):
        results = self._load_data(results_dir)
        num_samples = int(results[20])
        data = self._clean_data(results, num_samples, self.specials)

        return self._return_data(data, num_samples, self.mode)

    @staticmethod
    def _load_data(results_dir):
        with open(str(results_dir), 'r') as f:
            return f.readlines()

    @staticmethod
    def _clean_data(results, num_samples, specials):
        results = results[22: 22 + num_samples + 1]
        results = ' '.join(results).lower()
        results_trans_table = results.maketrans(specials)
        clean_data = results.translate(results_trans_table)
        return np.fromstring(clean_data, sep=' ')

    @staticmethod
    def _return_data(data, num_samples, mode) -> np.array:
        if mode == 's':
            return data.reshape(num_samples, 1)
        if mode == 'v':
            return data.reshape(num_samples, 3)
