from matplotlib.cbook import pts_to_midstep
from qsurface.main import initialize, run, BenchmarkDecoder, run_multiprocess
from qsurface.decoders import mwpm
from os import listdir
from os.path import isfile, join
import pandas as pd

iters = 100

# SIZE = [(4,4), (6,6), (8,8), (12,12), (16,16)]
SIZE = [(4,4), (6,6), (8,8)]
ERRORS = [{"p_bitflip": 0.001, "p_phaseflip": 0.001},{"p_bitflip": 0.002, "p_phaseflip": 0.002},{"p_bitflip": 0.004, "p_phaseflip": 0.004},
{"p_bitflip": 0.006, "p_phaseflip": 0.006},{"p_bitflip": 0.008, "p_phaseflip": 0.008},{"p_bitflip": 0.01, "p_phaseflip": 0.01},
{"p_bitflip": 0.012, "p_phaseflip": 0.012},{"p_bitflip": 0.014, "p_phaseflip": 0.014},{"p_bitflip": 0.016, "p_phaseflip": 0.016},
{"p_bitflip": 0.018, "p_phaseflip": 0.018},{"p_bitflip": 0.02, "p_phaseflip": 0.02},{"p_bitflip": 0.022, "p_phaseflip": 0.022},
{"p_bitflip": 0.024, "p_phaseflip": 0.024},{"p_bitflip": 0.026, "p_phaseflip": 0.026},{"p_bitflip": 0.028, "p_phaseflip": 0.028},
{"p_bitflip": 0.03, "p_phaseflip": 0.03},{"p_bitflip": 0.032, "p_phaseflip": 0.032}]


plot_points = {}
for size in SIZE:
    plot_points[size] = []

for error in ERRORS:
    for size in SIZE:
        code, decoder = initialize(size, "planar", "unionfind", enabled_errors=["pauli"],faulty_measurements=True, initial_states=(0,0))
        benchmarker = BenchmarkDecoder({
            "decode": ["duration", "value_to_list"],
            "correct_edge": "count_calls",})

        benchmark_data = run(code, decoder, iterations=iters, error_rates=error, benchmark=benchmarker, decode_initial=False)
        plot_points[size].append(benchmark_data["no_error"]/iters)
    


print(plot_points)

export_data = pd.DataFrame(plot_points)

export_data.to_json('C:/qarch/qsurface/data/exported_data/threshold_data_phenomenological.json')