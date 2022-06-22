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
                WEIGHT-3 ARCHITECTURE
   ####################################################'''

code, decoder = initialize((4,4), "weight_3_toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file="./qsurface/running/phenomenological_wt_3_toric_px_0.03_pz_0.03_prx_0.03_prz_0.03_pmx_0.03_pmz_0.03_ghz_1.csv", initial_states=(0,0))
benchmarker = BenchmarkDecoder({
        "decode": ["duration", "value_to_list"],
        "correct_edge": "count_calls",})
print(run(code, decoder, iterations=1000, decode_initial=False, benchmark=benchmarker))