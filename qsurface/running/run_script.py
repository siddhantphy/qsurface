from itertools import cycle
from queue import PriorityQueue
from random import seed
from re import S
from qsurface.main import initialize, run, run_multiprocess, run_multiprocess_superoperator, BenchmarkDecoder
from qsurface.decoders import mwpm



''' SUPEROPERATOR USAGE '''
code, decoder = initialize((4,4), "toric", "unionfind", plotting=True, superoperator_enable=True, sup_op_file="C:/qarch/qsurface/data/phenomenological/phenomenological_0.0_0.0_0.05_0.05_toric.csv", initial_states=(0,0))
benchmarker = BenchmarkDecoder({
        "decode": ["duration", "value_to_list"],
        "correct_edge": "count_calls",})
print(run(code, decoder, iterations=2, decode_initial=False, benchmark=benchmarker))



''' PHENOMENOLOGICAL ORIGINAL QSURFACE '''
# code, decoder = initialize((4,4), "toric", "unionfind", enabled_errors=["pauli"], plotting=True, initial_states=(0,0),layers=3, faulty_measurements=True)
# p_bitflip = 0.0
# p_phaseflip = 0.0
# p_bitflip_plaq = 0.05
# p_bitflip_star = 0.05
# benchmarker = BenchmarkDecoder({
#         "decode": ["duration", "value_to_list"],
#         "correct_edge": "count_calls",})

# print(run(code, decoder, iterations=1, error_rates={"p_bitflip": p_bitflip, "p_phaseflip": p_phaseflip, "p_bitflip_plaq": p_bitflip_plaq, "p_bitflip_star": p_bitflip_star},benchmark=benchmarker, decode_initial=False))

'''####################################################
                MULTI-PROCESSING
   ####################################################'''

# code, decoder = initialize((4,4), "toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file="C:/qarch/qsurface/data/phenomenological/phenomenological_0.03_0.03_0.03_0.03_toric.csv", initial_states=(0,0))
# if __name__ == "__main__":
        # print(run_multiprocess_superoperator(code, decoder, iterations=10000, decode_initial=False, seed=59))
        # run_multiprocess(code, decoder, iterations=100, decode_initial=False, seed=59, benchmark=benchmarker)
