from qsurface.main import initialize, run, BenchmarkDecoder
from qsurface.decoders import mwpm

code = initialize((5,5), "toric", "mwpm", superoperator_enabled=True, Superoperator="abcd")
print(code)

# run(code, decoder, iterations=10, error_rates = {"p_bitflip": 0.1})

# import sys
# print(sys.path)

import qsurface
print(qsurface.__file__)