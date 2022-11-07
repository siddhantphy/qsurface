import sys 
sys.path.append("c:\\qarch\\qsurface\\")

from qsurface.main import initialize, run, run_multiprocess, run_multiprocess_superoperator, BenchmarkDecoder

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

# code, decoder = initialize((4,4), "weight_0_toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file="./running/phenomenological_0.07_0.07_0.07_0.07_toric.csv", initial_states=(0,0))
code, decoder = initialize((4,4), "weight_3_toric", "unionfind",layers=15, plotting=False, superoperator_enable=True, sup_op_file="./running/phenomenological_wt_3_toric_px_0.07_pz_0.07_prx_0.07_prz_0.07_pmx_0.07_pmz_0.07_ghz_1.csv", initial_states=(0,0))
# code, decoder = initialize((4,4), "weight_4_toric", "unionfind",layers=15, plotting=False, superoperator_enable=True, sup_op_file="./running/phenomenological_wt_4_toric_px_0.07_pz_0.07_pmx_0.07_pmz_0.07_ghz_1.csv", initial_states=(0,0))

print(run(code, decoder, iterations=3000, decode_initial=False, benchmark=benchmarker))


# code, decoder = initialize((4,4), "toric", "unionfind",layers=15, plotting=False, enabled_errors=["pauli"], faulty_measurements=True)
# print(run(code, decoder, iterations=3000, error_rates = {"p_bitflip": 0.07, "p_phaseflip": 0.07, "p_bitflip_plaq": 0.07, "p_bitflip_star": 0.07}, benchmark=benchmarker))