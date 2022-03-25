from qsurface.main import initialize, run, run_multiprocess, run_multiprocess_superoperator, BenchmarkDecoder
from qsurface.decoders import mwpm



# code, decoder = initialize((2,2), "toric", "mwpm",enabled_errors=["pauli"], faulty_measurements=True, superoperator_enabled=False, sup_file="data/eg_sup.csv")

code, decoder = initialize((3,3), "toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file="C:/qarch/qsurface/data/phenomenological/phenomenological_0.03_0.03_0.03_0.03_toric.csv", initial_states=(0,0))
# code, decoder = initialize((3,3), "toric", "unionfind", enabled_errors=["pauli"], faulty_measurements=True, plotting=False, initial_states=(0,0))

# print(code.stars)

'''####################################################
                testing ones
   ####################################################'''
# code, decoder = initialize((4,4), "toric", "unionfind", plotting=True, superoperator_enable=True, sup_op_file="data/tests/test_east_star.csv", initial_states=(0,0))

# benchmarker = BenchmarkDecoder({
#         "decode": ["duration", "value_to_list"],
#         "correct_edge": "count_calls",})



# def tracefunc(frame, event, arg, indent=[0]):
#       if event == "call":
#           indent[0] += 2
#           print("-" * indent[0] + "> call function", frame.f_code.co_name)
#       elif event == "return":
#           print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
#           indent[0] -= 2
#       return tracefunc

# import sys
# func_read = sys.setprofile(tracefunc)

# print(code)
# print(decoder)

# run(code, decoder, iterations=1, error_rates = {"p_bitflip": 0.1})

# print(func_read)



# print(run_multiprocess(code, decoder, iterations=80, benchmark=benchmarker, decode_initial=False, seed=59))

# run(code, decoder, iterations=10, error_rates = {"p_bitflip": 0.1}, benchmark=benchmarker)


# p_bitflip = 0.03
# p_phaseflip = 0.03
# p_bitflip_plaq = 0.03
# p_bitflip_star = 0.03
# print(run(code, decoder, iterations=1, error_rates={"p_bitflip": p_bitflip, "p_phaseflip": p_phaseflip, "p_bitflip_plaq": p_bitflip_plaq, "p_bitflip_star": p_bitflip_star}, decode_initial=False))
# print(run_multiprocess(code, decoder, iterations=1, error_rates={"p_bitflip": p_bitflip, "p_phaseflip": p_phaseflip, "p_bitflip_plaq": p_bitflip_plaq, "p_bitflip_star": p_bitflip_star}, decode_initial=False))

# print(run(code, decoder, iterations=100, decode_initial=False))

# print(benchmarker.lists)
# print(benchmarker.data)

print(run(code, decoder, iterations=10000, decode_initial=False, seed=59))

'''####################################################
                MULTI-PROCESSING
   ####################################################'''

# code, decoder = initialize((3,3), "toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file="C:/qarch/qsurface/data/phenomenological/phenomenological_0.03_0.03_0.03_0.03_toric.csv", initial_states=(0,0))
# if __name__ == "__main__":
#         print(run_multiprocess_superoperator(code, decoder, iterations=10000, decode_initial=False, seed=59))