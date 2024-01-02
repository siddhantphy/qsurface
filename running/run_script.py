import sys 
sys.setrecursionlimit(1000000)
# sys.path.append("c:\\qarch\\qsurface\\")

from qsurface.main import initialize, run, run_multiprocess, run_multiprocess_superoperator, BenchmarkDecoder
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np

''' SUPEROPERATOR USAGE '''
# code, decoder = initialize((8,8), "toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file="./data/phenomenological/phenomenological_0.0081995_0.0081995_0.032_0.032_toric.csv", initial_states=(0,0))
# benchmarker = BenchmarkDecoder({
#         "decode": ["duration", "value_to_list"],
#         "correct_edge": "count_calls",})
# print(run(code, decoder, iterations=20, decode_initial=False, benchmark=benchmarker, seed=59))



''' PHENOMENOLOGICAL ORIGINAL QSURFACE '''
# code, decoder = initialize((10,10), "toric", "unionfind", enabled_errors=["pauli"], plotting=False, initial_states=(0,0), faulty_measurements=True)
# p_bitflip = 0.0
# p_phaseflip = 0.0
# p_bitflip_plaq = 0.05
# p_bitflip_star = 0.05
# benchmarker = BenchmarkDecoder({
#         "decode": ["duration", "value_to_list"],
#         "correct_edge": "count_calls",})

# # print(run(code, decoder, iterations=1, error_rates={"p_bitflip": p_bitflip, "p_phaseflip": p_phaseflip, "p_bitflip_plaq": p_bitflip_plaq, "p_bitflip_star": p_bitflip_star},benchmark=benchmarker, decode_initial=False))
# if __name__ == "__main__":
#         run_multiprocess(code, decoder, iterations=100,error_rates={"p_bitflip": p_bitflip, "p_phaseflip": p_phaseflip, "p_bitflip_plaq": p_bitflip_plaq, "p_bitflip_star": p_bitflip_star}, decode_initial=False, seed=59, benchmark=benchmarker)
'''####################################################
                MULTI-PROCESSING SUPEROPERATOR
   ####################################################'''

#code, decoder = initialize((8,8), "toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file="./data/phenomenological/phenomenological_0.0081995_0.0081995_0.032_0.032_toric.csv", initial_states=(0,0))

#benchmarker = BenchmarkDecoder({
#        "decode": ["duration", "value_to_list"],
#        "correct_edge": "count_calls",})
#if __name__ == '__main__':
#        print(run_multiprocess(code, decoder, iterations=20, decode_initial=False, benchmark=benchmarker, seed=59))
#        print(benchmarker.data)
#        # print(run_multiprocess_superoperator(code, decoder, iterations=100, decode_initial=False, benchmark=benchmarker))

'''####################################################
                WEIGHT-X ARCHITECTURES
   ####################################################'''
benchmarker = BenchmarkDecoder({
"decode": ["duration", "value_to_list"],
"correct_edge": "count_calls"})
iters=1000

# code, decoder = initialize((8,8), "weight_0_toric", "unionfind",layers=1, plotting=False, superoperator_enable=True, sup_op_file="./running/phenomenological_wt_0_toric_rates_px_0.03_pz_0.03_pmx_0.03_pmz_0.03.csv", initial_states=(0,0))
# code, decoder = initialize((20,20), "weight_3_toric", "mwpm",layers=100, plotting=False, superoperator_enable=True, sup_op_file="./running/phenomenological_wt_3_toric_rates_px_0.09_pz_0.09_prx_0.09_prz_0.09_pmx_0_pmz_0_ghz_1.csv", initial_states=(0,0))
# 1M case
code, decoder = initialize((6,6), "weight_3_toric", "mwpm", plotting=False, superoperator_enable=True, sup_op_file="./running/20231109_071924_hc_weight_3_direct_node-ss1eq_network_noise_type-60_p_g-0.002_p_m-0.002_cut_off_time-0.0041641_merged.csv", initial_states=(0,0), seed=500)
# 1.75M case
# code, decoder = initialize((6,6), "weight_3_toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file="./running/20231109_071925_hc_weight_3_direct_node-ss1eq_network_noise_type-60_p_g-0.002_p_m-0.002_cut_off_time-0.0041641_merged.csv", initial_states=(0,0), seed=500)

print(run(code, decoder, iterations=iters,decode_initial=True, benchmark=benchmarker)['no_error']/iters)

# print(code.data_qubits[0][(0.5,0)].edges['z'].nodes)

# print(code.rounds_plaq[0][1].round_ancillas[0].parity_qubits)

# code, decoder = initialize((6,6), "toric", "unionfind",layers=2, plotting=False, enabled_errors=["pauli"], faulty_measurements=True)
# print(run(code, decoder, iterations=10000,decode_initial=True, error_rates = {"p_bitflip": 0.09, "p_phaseflip": 0.09, "p_bitflip_plaq": 0, "p_bitflip_star": 0 }, benchmark=benchmarker))

'''####################################################
        WEIGHT-X ARCHITECTURES' VERIFICATION
   ####################################################'''

# ERROR_RATES = [0, 0.001, 0.002, 0.006, 0.008, 0.010, 0.012, 0.014, 0.016, 0.018, 0.020, 0.022, 0.024, 0.026, 0.027, 0.028, 0.029, 0.030, 0.032, 0.034, 0.036]
# SIZES = [(4,4), (6,6), (8,8), (10,10)]
# 0.83 [2]

# iterations = 8
# error_rates = [float(round(x,3)) for x in np.linspace(0.0, 0.12, 30)]
# SIZES = [(4,4)]
# benchmarker = BenchmarkDecoder({
# "decode": ["duration", "value_to_list"],
# "correct_edge": "count_calls"})


# for num, architecture in zip([0,4,3,-1],["weight_0_toric", "weight_4_toric", "weight_3_toric", "toric"]):
#         plot_points = {}
#         for size in SIZES:
#                 plot_points[size] = []
#         file_location = f"./data/weight_{num}_phenomenological_verify/"
#         export_location = f'./data/weight_{num}_phenomenological_verify/computed_data/threshold_{architecture}_superoperator_data.json'
#         files = [f for f in listdir(file_location) if isfile(join(file_location, f))]
#         FILES = [file_location + f for f in files]

#         for size in SIZES:
#                 for rate in error_rates:
#                         if num == -1:
#                                 code, decoder = initialize(size, architecture, "unionfind",enabled_errors=["pauli"], initial_states=(0,0))
#                                 if __name__ == '__main__':
#                                         no_error = run(code, decoder, iterations=iterations, error_rates = {"p_bitflip": rate, "p_phaseflip": rate})["no_error"]
#                                         plot_points[size].append((rate, no_error /iterations))
#                         else:
#                                 super_op = "NA"
#                                 tmp_files_rates = [float(file[file.find("_px_")+len("_px_"):file.rfind("_pz_")]) for file in FILES]
#                                 for f_rate, sup in zip(tmp_files_rates, FILES):
#                                         if rate == f_rate:
#                                                 super_op = sup
#                                 code, decoder = initialize(size, architecture, "unionfind", layers=1, superoperator_enable=True, sup_op_file=super_op, initial_states=(0,0))
#                                 if __name__ == '__main__':
#                                         no_error = run(code, decoder, iterations=iterations)["no_error"]
#                                         plot_points[size].append((rate, no_error /iterations))

#         export_data = pd.DataFrame(plot_points)

#         export_data.to_json(export_location)