from qsurface.main import initialize, run, BenchmarkDecoder
from qsurface.decoders import mwpm



# code, decoder = initialize((2,2), "toric", "mwpm",enabled_errors=["pauli"], faulty_measurements=True, superoperator_enabled=False, sup_file="data/eg_sup.csv")
code, decoder = initialize((6,4), "toric", "mwpm", plotting=False, superoperator_enable=True, sup_op_file="data/eg_sup.csv")
# code, decoder = initialize((6,4), "toric", "mwpm", plotting=True, superoperator_enable=True, sup_op_file="data/eg_sup.csv",initial_states=(0,0))
# code, decoder = initialize((4,4), "toric", "mwpm", enabled_errors=["pauli"], faulty_measurements=True, plotting=True)
# code, decoder = initialize((3,3), "toric", "mwpm", enabled_errors=["pauli"], faulty_measurements=True, plotting=True, initial_states=(0,1))
# code, decoder = initialize((2,2), "toric", "mwpm", enabled_errors=["pauli"], faulty_measurements=True, plotting=True)



print(code.errors)
print(code.superoperator_errors_list)



code.init_superoperator_errors()
print(code.superoperator_errors_list)



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



# run(code, decoder, iterations=1, error_rates = {"p_bitflip": 0.1}, decode_initial=False)