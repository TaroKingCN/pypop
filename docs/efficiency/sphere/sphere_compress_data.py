import os
import sys
import pickle

import numpy as np
from pypop7.optimizers.core import optimizer
sys.modules['optimizer'] = optimizer  # for `pickle`


def io_pickle(i, i_o, results=None):
    afile = os.path.join('./', 'DEAP-PSO_' + i + '.pickle')
    if i_o == 'r':
        with open(afile, 'rb') as handle:
            return pickle.load(handle)
    else:
        with open(afile, 'wb') as handle:  # to save all data in .pickle format
            pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)


def compress_fitness(fitness):
    # use 1-based index
    index = np.arange(1, fitness.shape[0], 2000)
    # recover 0-based index via - 1
    index = np.append(index, fitness.shape[0]) - 1
    self_fitness = np.stack((index, fitness[index, 1]), 1)
    # recover 1-based index
    self_fitness[0, 0], self_fitness[-1, 0] = 1, len(fitness)
    return self_fitness


if __name__ == '__main__':
    s_trials, end_trials = 1, 10
    funcs = ['sphere']
    for f in funcs:
        for i in range(s_trials, end_trials + 1):
            results = io_pickle(str(i), 'r')
            results['fitness'] = compress_fitness(results['fitness'])
            io_pickle(str(i), 'w', results)
