from qsurface.main import initialize, run, BenchmarkDecoder
from qsurface.decoders import mwpm



# code, decoder = initialize((2,2), "toric", "mwpm",enabled_errors=["pauli"], faulty_measurements=True, superoperator_enabled=False, sup_file="data/eg_sup.csv")
code, decoder = initialize((4,6), "planar", "unionfind", plotting=True, superoperator_enable=True, sup_op_file="data/eg_sup.csv", initial_states=(0,0))
# code, decoder = initialize((6,4), "toric", "mwpm", plotting=False, superoperator_enable=True, sup_op_file="data/eg_sup.csv",initial_states=(0,0))
# code, decoder = initialize((4,4), "toric", "mwpm", enabled_errors=["pauli"], faulty_measurements=True, plotting=True)
# code, decoder = initialize((3,3), "toric", "mwpm", enabled_errors=["pauli"], faulty_measurements=True, plotting=True, initial_states=(0,1))
# code, decoder = initialize((6,6), "toric", "mwpm", enabled_errors=["pauli"], faulty_measurements=True, plotting=False)

# print(code.stars)

'''####################################################
                testing ones
   ####################################################'''
# code, decoder = initialize((4,4), "toric", "unionfind", plotting=True, superoperator_enable=True, sup_op_file="data/tests/test_east_star.csv", initial_states=(0,0))

benchmarker = BenchmarkDecoder({
        "decode": ["duration", "value_to_list"],
        "correct_edge": "count_calls",})

# print(code.errors)
# print("######################")
# print(code.superoperator_errors_list)
# print(code.stars)
# print(code.plaquettes)

# print("######################")

# code.init_superoperator_errors()

# print(code.superoperator_errors_list)
# print(code.stars)
# print(code.plaquettes)



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



run(code, decoder, iterations=10, benchmark=benchmarker, decode_initial=False, seed=69)

# run(code, decoder, iterations=10, error_rates = {"p_bitflip": 0.1}, benchmark=benchmarker)

print(benchmarker.lists)