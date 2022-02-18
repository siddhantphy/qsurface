import pytest
from qsurface.codes._template.sim import SuperOperator
import pandas as pd


@pytest.fixture
def example_superoperator_data():
    '''Example data for superoperator'''
    eg_data = pd.read_csv("data/eg_sup.csv", sep=';')
    return eg_data



# test_sup = SuperOperator()

def test_initialize_superoperator():
    pass