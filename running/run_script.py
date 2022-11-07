import sys 
sys.path.append("c:\\qarch\\qsurface\\")

from qsurface.main import initialize, run, run_multiprocess, run_multiprocess_superoperator, BenchmarkDecoder
from os import listdir
from os.path import isfile, join
import pandas as pd

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
# benchmarker = BenchmarkDecoder({
# "decode": ["duration", "value_to_list"],
# "correct_edge": "count_calls"})

# code, decoder = initialize((2,2), "weight_0_toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file="./running/phenomenological_0.07_0.07_0.07_0.07_toric.csv", initial_states=(0,0))
# code, decoder = initialize((4,4), "weight_3_toric", "unionfind",layers=15, plotting=False, superoperator_enable=True, sup_op_file="./running/phenomenological_wt_3_toric_px_0.07_pz_0.07_prx_0.07_prz_0.07_pmx_0.07_pmz_0.07_ghz_1.csv", initial_states=(0,0))
# code, decoder = initialize((4,4), "weight_4_toric", "unionfind",layers=15, plotting=False, superoperator_enable=True, sup_op_file="./running/phenomenological_wt_4_toric_px_0.07_pz_0.07_pmx_0.07_pmz_0.07_ghz_1.csv", initial_states=(0,0))
# if __name__ == '__main__':
#         print(run_multiprocess_superoperator(code, decoder, iterations=8, decode_initial=False, benchmark=benchmarker)['no_error'])


# code, decoder = initialize((4,4), "toric", "unionfind",layers=15, plotting=False, enabled_errors=["pauli"], faulty_measurements=True)
# print(run(code, decoder, iterations=3000, error_rates = {"p_bitflip": 0.07, "p_phaseflip": 0.07, "p_bitflip_plaq": 0.07, "p_bitflip_star": 0.07}, benchmark=benchmarker))


'''####################################################
        WEIGHT-X ARCHITECTURES' VERIFICATION
   ####################################################'''

iterations = 2
ERROR_RATES = [0, 0.001, 0.002, 0.006, 0.008, 0.010, 0.012, 0.014, 0.016, 0.018, 0.020, 0.022, 0.024, 0.026, 0.027, 0.028, 0.029, 0.030, 0.032, 0.034, 0.036]
SIZES = [(4,4), (6,6), (8,8), (10,10), (12,12), (14,14), (16,16)]
benchmarker = BenchmarkDecoder({
"decode": ["duration", "value_to_list"],
"correct_edge": "count_calls"})


for num, architecture in zip([0,4,3],["weight_0_toric", "weight_4_toric", "weight_3_toric"]):
        plot_points = {}
        for size in SIZES:
                plot_points[size] = []
        file_location = f"./data/weight_{num}_phenomenological_verify/"
        export_location = f'./data/weight_{num}_phenomenological_verify/computed_data/threshold_{architecture}_superoperator_data.json'
        files = [f for f in listdir(file_location) if isfile(join(file_location, f))]
        FILES = [file_location + f for f in files]

        for size in SIZES:
                for rate, super_op in zip(ERROR_RATES, FILES):
                        print(rate)
                        code, decoder = initialize(size, architecture, "unionfind", superoperator_enable=True, sup_op_file=super_op, initial_states=(0,0))
                        if __name__ == '__main__':
                                benchmark_data = run_multiprocess_superoperator(code, decoder, iterations=iterations, decode_initial=False)
                        plot_points[size].append((rate, benchmark_data["no_error"]/iterations))

        export_data = pd.DataFrame(plot_points)

        export_data.to_json(export_location)