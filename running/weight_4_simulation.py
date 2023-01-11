import sys 
sys.setrecursionlimit(1000000)
# sys.path.append("c:\\qarch\\qsurface\\")

from qsurface.main import initialize, run, run_multiprocess, run_multiprocess_superoperator, BenchmarkDecoder
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np

# Find error rates from the superoperator files!
# file_location = f"./data/weight_4_scattering/"
file_location = f"./data/weight_4_emission/"
files = [f for f in listdir(file_location) if isfile(join(file_location, f))]
sup_files = [file_location + f for f in files]
error_rates = [float(file[file.find("p_g-")+len("p_g-"):file.rfind("_p_m")]) for file in sup_files]
errors = sorted(error_rates, key=float)


iterations = 5
SIZES = [(4,4), (6, 6), (8, 8), (10, 10), (12, 12) ]
benchmarker = BenchmarkDecoder({
"decode": ["duration", "value_to_list"],
"correct_edge": "count_calls"})


plot_points = {}
for size in SIZES:
        plot_points[size] = []
file_location = f"./data/weight_4_emission/"
export_location = f'./data/weight_4_emission/computed_data/threshold_weight_4_Scattering_superoperator_data.json'
files = [f for f in listdir(file_location) if isfile(join(file_location, f))]

for size in SIZES:
        for rate in errors:
                super_op = "NA"
                tmp_filess = [float(file[file.find("p_g-")+len("p_g-"):file.rfind("_p_m")]) for file in sup_files]
                for f_rate, sup in zip(tmp_filess, sup_files):
                        if rate == f_rate:
                                super_op = sup
                code, decoder = initialize(size, "weight_4_toric", "unionfind", superoperator_enable=True, sup_op_file=super_op, initial_states=(0,0))
                if __name__ == '__main__':
                        no_error = run(code, decoder, iterations=iterations)["no_error"]
                        plot_points[size].append((rate, no_error /iterations))

export_data = pd.DataFrame(plot_points)

export_data.to_json(export_location)