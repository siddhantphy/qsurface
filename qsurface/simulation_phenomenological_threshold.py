from matplotlib.cbook import pts_to_midstep
from qsurface.main import initialize, run, BenchmarkDecoder, run_multiprocess
from qsurface.decoders import mwpm
from os import listdir
from os.path import isfile, join
import pandas as pd


export_location = './data/exported_data/threshold_superoperator_data_4_4.json'
iters = 60000

SIZE = [(4,4)]
# ERRORS = [{"p_bitflip": 0.024, "p_phaseflip": 0.024, "p_bitflip_plaq": 0.024, "p_bitflip_star": 0.024}]
ERRORS = [{"p_bitflip": 0.005, "p_phaseflip": 0.005, "p_bitflip_plaq": 0.005, "p_bitflip_star": 0.005},
{"p_bitflip": 0.01, "p_phaseflip": 0.01, "p_bitflip_plaq": 0.01, "p_bitflip_star": 0.01},
{"p_bitflip": 0.015, "p_phaseflip": 0.015, "p_bitflip_plaq": 0.015, "p_bitflip_star": 0.015},
{"p_bitflip": 0.02, "p_phaseflip": 0.02, "p_bitflip_plaq": 0.02, "p_bitflip_star": 0.02},
{"p_bitflip": 0.025, "p_phaseflip": 0.025, "p_bitflip_plaq": 0.025, "p_bitflip_star": 0.025},
{"p_bitflip": 0.03, "p_phaseflip": 0.03, "p_bitflip_plaq": 0.03, "p_bitflip_star": 0.03},
{"p_bitflip": 0.035, "p_phaseflip": 0.035, "p_bitflip_plaq": 0.035, "p_bitflip_star": 0.035},
{"p_bitflip": 0.04, "p_phaseflip": 0.04, "p_bitflip_plaq": 0.04, "p_bitflip_star": 0.04}
]


plot_points = {}
for size in SIZE:
    plot_points[size] = []

for size in SIZE:
    for error in ERRORS:
        code, decoder = initialize(size, "toric", "unionfind", enabled_errors=["pauli"],faulty_measurements=True, initial_states=(0,0))
        benchmarker = BenchmarkDecoder({
            "decode": ["duration", "value_to_list"],
            "correct_edge": "count_calls",})

        benchmark_data = run(code, decoder, iterations=iters, error_rates=error, benchmark=benchmarker, decode_initial=False)
        plot_points[size].append(benchmark_data["no_error"]/iters)
    


print(plot_points)

export_data = pd.DataFrame(plot_points)

export_data.to_json(export_location)