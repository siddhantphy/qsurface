from qsurface.main import initialize, run, run_multiprocess, run_multiprocess_superoperator, BenchmarkDecoder

''' SUPEROPERATOR USAGE '''
code, decoder = initialize((4,4), "toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file="C:/qarch/qsurface/data/phenomenological/phenomenological_0.0081995_0.0081995_0.032_0.032_toric.csv", initial_states=(0,0))
benchmarker = BenchmarkDecoder({
        "decode": ["duration", "value_to_list"],
        "correct_edge": "count_calls",})
print(run(code, decoder, iterations=2, decode_initial=False, benchmark=benchmarker))



''' PHENOMENOLOGICAL ORIGINAL QSURFACE '''
# code, decoder = initialize((4,4), "toric", "unionfind", enabled_errors=["pauli"], plotting=False, initial_states=(0,0), faulty_measurements=True)
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

# code, decoder = initialize((4,4), "toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file="C:/qarch/qsurface/data/phenomenological/phenomenological_0.0081995_0.0081995_0.032_0.032_toric.csv", initial_states=(0,0))
# benchmarker = BenchmarkDecoder({
#         "decode": ["duration", "value_to_list"],
#         "correct_edge": "count_calls",})
# if __name__ == '__main__':
#         print(run_multiprocess_superoperator(code, decoder, iterations=100, decode_initial=False, benchmark=benchmarker))





# print("#############")
# print(code.superoperator_errors_list)
# print(code.plaquettes)
# print(code.stars)
# print("#############")
# jkldfn;sodfn'skldmng;ksdfg