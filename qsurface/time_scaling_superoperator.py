from time import time
from qsurface.main import initialize, run, BenchmarkDecoder
from qsurface.decoders import mwpm
from os import listdir
from os.path import isfile, join
import pandas as pd
import timeit


file_location = "./data/weight_3_phenomenological/"
export_location = './data/weight_3_phenomenological/exported_data/time_scaling_weight3.json'
iters = 100


SIZE = [(4,4), (6,6), (8,8), (10,10), (12,12), (14,14), (16,16)]
files = [f for f in listdir(file_location) if isfile(join(file_location, f))]
FILES = [file_location + f for f in files]
N_RATE = len(FILES)

time_comp = {}
for serial in range(N_RATE):
    time_comp[serial] = []


for super, serial in zip(FILES, range(N_RATE)):
    for size in SIZE:
        start = timeit.default_timer()
        code, decoder = initialize(size, "weight_3_toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file=super, initial_states=(0,0))
        run(code, decoder, iterations=iters, decode_initial=False)
        stop = timeit.default_timer()
        duration = stop - start

        time_comp[serial].append(duration/iters)

print(time_comp)
export_data = pd.DataFrame(time_comp)

export_data.to_json(export_location)