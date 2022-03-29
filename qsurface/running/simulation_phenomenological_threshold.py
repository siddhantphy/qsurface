from matplotlib.cbook import pts_to_midstep
from qsurface.main import initialize, run, BenchmarkDecoder, run_multiprocess
from qsurface.decoders import mwpm
from os import listdir
from os.path import isfile, join
import pandas as pd

iters = 30000

SIZE = [(6,6), (8,8), (10,10), (12,12)]
ERRORS = [{"p_bitflip": 0.0, "p_phaseflip": 0.03, "p_bitflip_plaq": 0.0, "p_bitflip_star": 0.0},
{"p_bitflip": 0.0, "p_phaseflip": 0.04, "p_bitflip_plaq": 0.0, "p_bitflip_star": 0.0},
{"p_bitflip": 0.0, "p_phaseflip": 0.06, "p_bitflip_plaq": 0.0, "p_bitflip_star": 0.0},
{"p_bitflip": 0.0, "p_phaseflip": 0.08, "p_bitflip_plaq": 0.0, "p_bitflip_star": 0.0},
{"p_bitflip": 0.0, "p_phaseflip": 0.09, "p_bitflip_plaq": 0.0, "p_bitflip_star": 0.0},
{"p_bitflip": 0.0, "p_phaseflip": 0.10, "p_bitflip_plaq": 0.0, "p_bitflip_star": 0.0},
{"p_bitflip": 0.0, "p_phaseflip": 0.105, "p_bitflip_plaq": 0.0, "p_bitflip_star": 0.0},
{"p_bitflip": 0.0, "p_phaseflip": 0.11, "p_bitflip_plaq": 0.0, "p_bitflip_star": 0.0},
{"p_bitflip": 0.0, "p_phaseflip": 0.12, "p_bitflip_plaq": 0.0, "p_bitflip_star": 0.0},
{"p_bitflip": 0.0, "p_phaseflip": 0.13, "p_bitflip_plaq": 0.0, "p_bitflip_star": 0.0}]


plot_points = {}
for size in SIZE:
    plot_points[size] = []

for size in SIZE:
    for error in ERRORS:
        code, decoder = initialize(size, "toric", "unionfind", enabled_errors=["pauli"],faulty_measurements=False, initial_states=(0,0))
        benchmarker = BenchmarkDecoder({
            "decode": ["duration", "value_to_list"],
            "correct_edge": "count_calls",})

        benchmark_data = run(code, decoder, iterations=iters, error_rates=error, benchmark=benchmarker, decode_initial=False)
        plot_points[size].append(benchmark_data["no_error"]/iters)
    


print(plot_points)

export_data = pd.DataFrame(plot_points)

export_data.to_json('C:/qarch/qsurface/data/exported_data/threshold_data_phenomenological.json')