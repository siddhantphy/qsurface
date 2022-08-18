from time import time
from qsurface.main import initialize, run, BenchmarkDecoder
from qsurface.decoders import mwpm
from os import listdir
from os.path import isfile, join
import pandas as pd
import timeit

export_location = './data/exported_data/time_scaling.json'
iters = 1000


SIZE = [(4,4), (6,6), (8,8), (10,10), (12,12), (14,14), (16,16)]
ERRORS = [{"p_bitflip": 0.005, "p_phaseflip": 0.005, "p_bitflip_plaq": 0.005, "p_bitflip_star": 0.005},
{"p_bitflip": 0.01, "p_phaseflip": 0.01, "p_bitflip_plaq": 0.01, "p_bitflip_star": 0.01},
{"p_bitflip": 0.015, "p_phaseflip": 0.015, "p_bitflip_plaq": 0.015, "p_bitflip_star": 0.015},
{"p_bitflip": 0.02, "p_phaseflip": 0.02, "p_bitflip_plaq": 0.02, "p_bitflip_star": 0.02},
{"p_bitflip": 0.025, "p_phaseflip": 0.025, "p_bitflip_plaq": 0.025, "p_bitflip_star": 0.025},
{"p_bitflip": 0.03, "p_phaseflip": 0.03, "p_bitflip_plaq": 0.03, "p_bitflip_star": 0.03},
{"p_bitflip": 0.035, "p_phaseflip": 0.035, "p_bitflip_plaq": 0.035, "p_bitflip_star": 0.035},
{"p_bitflip": 0.04, "p_phaseflip": 0.04, "p_bitflip_plaq": 0.04, "p_bitflip_star": 0.04}
]
N_RATE = len(ERRORS)

time_comp = {}
for serial in range(N_RATE):
    time_comp[serial] = []


for error, serial in zip(ERRORS, range(N_RATE)):
    for size in SIZE:
        start = timeit.default_timer()
        code, decoder = initialize(size, "toric", "unionfind", enabled_errors=["pauli"],faulty_measurements=True, initial_states=(0,0))
        run(code, decoder, iterations=iters, error_rates=error, decode_initial=False)
        stop = timeit.default_timer()
        duration = stop - start

        time_comp[serial].append(duration/iters)

print(time_comp)
export_data = pd.DataFrame(time_comp)

export_data.to_json(export_location)