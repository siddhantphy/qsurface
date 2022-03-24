from doctest import testfile
from pickletools import pyset
import pytest
import pandas as pd
from os import listdir
from os.path import isfile, join
from qsurface.main import initialize, run, BenchmarkDecoder
from qsurface.decoders import mwpm

files = [f for f in listdir("data/tests") if isfile(join("data/tests", f))]
FILES = ["data/tests/"+ f for f in files]


SIZES = [(i,j) for i, j in zip(range(2, 5),range(2, 5))]

@pytest.mark.parametrize("size", SIZES)
@pytest.mark.parametrize("lattice", ["toric", "planar"])
@pytest.mark.parametrize("dec", ["mwpm", "unionfind"])
@pytest.mark.parametrize("sup_op_file", FILES)
def test_directions(size, lattice, dec, testfile):
    code, decoder = initialize(size, lattice, dec, plotting=False, superoperator_enable=True, sup_op_file=testfile)
    assert type(code.superoperator_errors_list) == dict

def test__superoperator_verification_wth_seed():
    code, decoder = initialize((5,5), "toric", "unionfind", plotting=False, superoperator_enable=True, sup_op_file="C:/qarch/qsurface/data/phenomenological/phenomenological_0.0_0.03_0.0_0.0_toric.csv", initial_states=(0,0))
    benchmarker = BenchmarkDecoder({
        "decode": ["duration", "value_to_list"],
        "correct_edge": "count_calls",})
    benchmark_data = run(code, decoder, iterations=10000,benchmark=benchmarker, decode_initial=False, seed=59)
    assert benchmark_data["no_error"] == 2821