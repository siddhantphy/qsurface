from doctest import testfile
from pickletools import pyset
import pytest
import pandas as pd
from os import listdir
from os.path import isfile, join
from qsurface.main import initialize, run, BenchmarkDecoder
from qsurface.decoders import mwpm

TESTFILES = [f for f in listdir("data/tests") if isfile(join("data/tests", f))]
SIZ = [(i,j) for i, j in zip(range(2, 5),range(2, 5))]

@pytest.fixture
def superoperator_data():
    '''Example data for superoperator'''
    testfiles = [f for f in listdir("data/tests") if isfile(join("data/tests", f))]
    new = ["data/tests/" + s for s in testfiles]
    return testfiles

@pytest.fixture
def sizes():
    siz = [(i,j) for i, j in zip(range(2, 5),range(2, 5))]
    return siz

@pytest.mark.parametrize("size", SIZ)
@pytest.mark.parametrize("lattice", ["toric", "planar"])
@pytest.mark.parametrize("dec", ["mwpm", "unionfind"])
@pytest.mark.parametrize("sup_op_file", superoperator_data)
def test_directions(size, lattice, dec, testfile):
    code, decoder = initialize(size, lattice, dec, plotting=False, superoperator_enable=True, sup_op_file=testfile)
    assert type(code.superoperator_errors_list) == dict


# test_sup = SuperOperator()

def test_initialize_superoperator():
    pass

# print(superoperator_data())