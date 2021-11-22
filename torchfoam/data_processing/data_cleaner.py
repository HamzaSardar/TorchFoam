from typing import List, Dict

import numpy as np


class DataCleaner:

    def __init__(self, mode: str) -> None:

        """DataCleaner - converts an OpenFoam results file into a numpy array.

        Parameters
        ----------
        mode: str
            's' - Scalar mode.
            'v' - Vector mode.
        """
        self.mode = mode
        self.results = None
        self.specials = {'\n': ' ', '(': '', ')': '', ';': ''}

    def __call__(self, *args, **kwargs) -> np.array:
        return self.get(*args)

    def get(self, results_dir: str) -> np.array:

        """Function to run helper functions.

        Parameters
        ----------
        results_dir: str
            Path to ASCII results file.
        """

        results = self._load_data(results_dir)
        num_samples = int(results[20])
        data = self._clean_data(results, num_samples, self.specials)

        return self._return_data(data, num_samples, self.mode)

    @staticmethod
    def _load_data(results_dir: str) -> List[str]:

        """Helper function to load and return results file.

        Parameters
        ----------
        results_dir: str
            Path to ASCII results file.

        Returns
        -------
        List[str]
            Text file as list of (str) lines.
        """

        with open(str(results_dir), 'r') as f:
            return f.readlines()

    @staticmethod
    def _clean_data(results: List[str], num_samples: int, specials: Dict[str, str]) -> np.array:

        """Helper function to clean data and convert to numpy array of floats.

        Parameters
        ----------
        results: List[str]
            Results file in specified format.
        num_samples: int
            Number of data points.
        specials: Dict[str, str]
            Characters to remove are passed as keys, with values set as ''.

        Returns
        -------
        numpy.array
            Results data in numpy format.
        """

        results = results[22: 22 + num_samples + 1]
        results = ' '.join(results).lower()
        results_trans_table = results.maketrans(specials)
        clean_data = results.translate(results_trans_table)
        return np.fromstring(clean_data, sep=' ')

    @staticmethod
    def _return_data(data: np.array, num_samples: int, mode: str) -> np.array:

        """Helper function to return numpy.array data in required shape.

        Parameters
        ----------
        data: np.array
            Results data.
        num_samples: int
            Number of data points.
        mode: str
            's' - Scalar mode.
            'v' - Vector mode.

        Returns
        -------
        np.array
            Results, in numpy array of required shape.
        """

        if mode == 's':
            return data.reshape(num_samples, 1)
        if mode == 'v':
            return data.reshape(num_samples, 3)
