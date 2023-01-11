import sys 
sys.setrecursionlimit(100000000)
# sys.path.append("c:\\qarch\\qsurface\\")

from qsurface.main import initialize, run, run_multiprocess, run_multiprocess_superoperator, BenchmarkDecoder
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np

'''####################################################
        WEIGHT-X ARCHITECTURES' VERIFICATION
   ####################################################'''
# ERROR_RATES = [0, 0.001, 0.002, 0.006, 0.008, 0.010, 0.012, 0.014, 0.016, 0.018, 0.020, 0.022, 0.024, 0.026, 0.027, 0.028, 0.029, 0.030, 0.032, 0.034, 0.036]
# SIZES = [(4,4), (6,6), (8,8), (10,10)]
# for num, architecture in zip([0,4,3,-1],["weight_0_toric", "weight_4_toric", "weight_3_toric", "toric"]):




iterations = 1
SIZES = [(8,8)]
benchmarker = BenchmarkDecoder({
"decode": ["duration", "value_to_list"],
"correct_edge": "count_calls"})

ERRORS = [0.0, 0.001, 0.002, 0.006, 0.008, 0.01, 0.012, 0.014, 0.016, 0.018, 0.02, 0.022, 0.024, 0.026, 0.027, 0.028, 0.029, 0.03, 0.032, 0.034, 0.036]

for num, architecture in zip([0,4,3,-1],["weight_0_toric", "weight_4_toric", "weight_3_toric", "toric"]):
    plot_points = {}
    for size in SIZES:
        plot_points[size] = []
            
    file_location = f"./data/weight_{num}_phenomenological_verify/"
    files = [f for f in listdir(file_location) if isfile(join(file_location, f))]
    sup_files = [file_location + f for f in files]
    error_rates = [float(file[file.find("_px_")+len("_px_"):file.rfind("_pz_")]) for file in sup_files]
    errors = sorted(error_rates, key=float)
    export_location = f'./data/weight_{num}_phenomenological_verify/computed_data/threshold_{architecture}_superoperator_data.json'


    for size in SIZES:
        for rate in ERRORS:
            if num == -1:
                code, decoder = initialize(size, architecture, "unionfind",enabled_errors=["pauli"],faulty_measurements=True, initial_states=(0,0))
                if __name__ == '__main__':
                    no_error = run(code, decoder, iterations=iterations, error_rates = {"p_bitflip": rate, "p_phaseflip": rate, "p_bitflip_plaq": rate, "p_bitflip_star": rate})["no_error"]
                    plot_points[size].append((rate, no_error /iterations))
            # else:
            #     super_op = "NA"
            #     tmp_files_rates = [float(file[file.find("_px_")+len("_px_"):file.rfind("_pz_")]) for file in sup_files]
            #     for f_rate, sup in zip(tmp_files_rates, sup_files):
            #             if rate == f_rate:
            #                     super_op = sup
            #     code, decoder = initialize(size, architecture, "unionfind", superoperator_enable=True, sup_op_file=super_op, initial_states=(0,0))
            #     if __name__ == '__main__':
            #         no_error = run(code, decoder, iterations=iterations)["no_error"]
            #         plot_points[size].append((rate, no_error /iterations))

    export_data = pd.DataFrame(plot_points)

    export_data.to_json(export_location)