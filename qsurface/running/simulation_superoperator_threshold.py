from matplotlib.cbook import pts_to_midstep
from qsurface.main import initialize, run, BenchmarkDecoder
from qsurface.decoders import mwpm
from os import listdir
from os.path import isfile, join
import pandas as pd

iters = 10000

SIZE = [(4,4),(5,5), (6,6), (8,8)]
files = [f for f in listdir("C:/qarch/qsurface/data/monolithic") if isfile(join("C:/qarch/qsurface/data/monolithic", f))]
FILES = ["C:/qarch/qsurface/data/monolithic/normalized/"+ f for f in files]


plot_points = {}
for size in SIZE:
    plot_points[size] = []

for super in FILES:
    for size in SIZE:
        code, decoder = initialize(size, "toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file=super, initial_states=(0,0))
        benchmarker = BenchmarkDecoder({
            "decode": ["duration", "value_to_list"],
            "correct_edge": "count_calls",})

        benchmark_data = run(code, decoder, iterations=iters, benchmark=benchmarker, decode_initial=False)
        plot_points[size].append(benchmark_data["no_error"]/iters)
    


print(plot_points)

export_data = pd.DataFrame(plot_points)

export_data.to_json('C:/qarch/qsurface/data/exported_data/threshold_superoperator_data.json')