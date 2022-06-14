from matplotlib.cbook import pts_to_midstep
from qsurface.main import initialize, run, BenchmarkDecoder
from qsurface.decoders import mwpm
from os import listdir
from os.path import isfile, join
import pandas as pd


file_location = "./data/phenomenological/faulty_threshold_toric/"
export_location = './data/exported_data/threshold_superoperator_data.json'
iters = 1


SIZE = [(4,4), (6,6), (8,8), (10,10), (12,12)]
files = [f for f in listdir(file_location) if isfile(join(file_location, f))]
FILES = [file_location + f for f in files]


plot_points = {}
for size in SIZE:
    plot_points[size] = []


for size in SIZE:
    for super in FILES:
        code, decoder = initialize(size, "toric", "mwpm", plotting=False, superoperator_enable=True, sup_op_file=super, initial_states=(0,0))
        benchmarker = BenchmarkDecoder({
            "decode": ["duration", "value_to_list"],
            "correct_edge": "count_calls",})

        benchmark_data = run(code, decoder, iterations=iters, benchmark=benchmarker, decode_initial=False)
        plot_points[size].append(benchmark_data["no_error"]/iters)
    


print(plot_points)

export_data = pd.DataFrame(plot_points)

export_data.to_json(export_location)