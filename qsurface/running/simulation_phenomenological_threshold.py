from matplotlib.cbook import pts_to_midstep
from qsurface.main import initialize, run, BenchmarkDecoder, run_multiprocess
from qsurface.decoders import mwpm
from os import listdir
from os.path import isfile, join
import pandas as pd

iters = 100000

SIZE = [(4,4), (5,5), (6,6), (7,7), (8,8)]
ERRORS = [{"p_bitflip": 0.024, "p_phaseflip": 0.024, "p_bitflip_plaq": 0.024, "p_bitflip_star": 0.024}]
# ERRORS = [{"p_bitflip": 0.024, "p_phaseflip": 0.024, "p_bitflip_plaq": 0.024, "p_bitflip_star": 0.024},
# {"p_bitflip": 0.026, "p_phaseflip": 0.026, "p_bitflip_plaq": 0.026, "p_bitflip_star": 0.026},
# {"p_bitflip": 0.028, "p_phaseflip": 0.028, "p_bitflip_plaq": 0.028, "p_bitflip_star": 0.028},
# {"p_bitflip": 0.030, "p_phaseflip": 0.030, "p_bitflip_plaq": 0.030, "p_bitflip_star": 0.030},
# {"p_bitflip": 0.032, "p_phaseflip": 0.032, "p_bitflip_plaq": 0.032, "p_bitflip_star": 0.032}]


plot_points = {}
for size in SIZE:
    plot_points[size] = []

for size in SIZE:
    for error in ERRORS:
        code, decoder = initialize(size, "toric", "mwpm", enabled_errors=["pauli"],faulty_measurements=True, initial_states=(0,0))
        benchmarker = BenchmarkDecoder({
            "decode": ["duration", "value_to_list"],
            "correct_edge": "count_calls",})

        benchmark_data = run(code, decoder, iterations=iters, error_rates=error, benchmark=benchmarker, decode_initial=False)
        plot_points[size].append(benchmark_data["no_error"]/iters)
    


print(plot_points)

export_data = pd.DataFrame(plot_points)

export_data.to_json('C:/qarch/qsurface/data/exported_data/threshold_data_phenomenological.json')