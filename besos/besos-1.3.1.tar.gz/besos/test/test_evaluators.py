import pytest

import eppy_funcs as ef
from evaluator import EvaluatorEP, EvaluatorSR, EvaluatorEH
import numpy as np
import pandas as pd
from parameters import RangeParameter, CategoryParameter, Parameter, FieldSelector
from problem import EPProblem, Problem, EHProblem
import pyehub_funcs as pf
import sampling

@pytest.fixture
def building():
    #returns the basic building
    return ef.get_building()

@pytest.fixture
def hub():
    #returns the basic hub
    return pf.get_hub()

@pytest.fixture
def problem():
    parameters = [Parameter(FieldSelector(object_name='Mass NonRes Wall Insulation', field_name='Thickness'))]
    objectives = ['Electricity:Facility', 'Gas:Facility'] # the default is just 'Electricity:Facility'

    problem=EPProblem(parameters, objectives) #EPP Problem automatically converts these to MeterReaders
    return problem

@pytest.fixture
def energyhub_df():
    df = pd.DataFrame(np.array([[200, 600],[600, 200]]),columns= ['p1','p2'])
    return df

@pytest.fixture
def energyplus_df():
    df = EPdf = pd.DataFrame(np.array([[0.5],[0.8]]),columns= ['p1'])
    return df

@pytest.fixture
def hub_problem():

    parameters = [['LINEAR_CAPITAL_COSTS','Boiler'],['LINEAR_CAPITAL_COSTS','CHP']]
    objectives = ['total_cost','total_carbon']

    problem = EHProblem(parameters, objectives)
    return problem

def test_evaluatorEP(building, problem):
    """To make sure EvaluatorEP can be initialised and works as intended"""

    evaluator = EvaluatorEP(problem, building)
    result = evaluator([0.5]) # run with thickness set to 0.5

    assert np.isclose(result[0], 1818735943.9307632) and np.isclose(result[1], 2172045529.871896), f'Unexpected result for EvaluatorEP, {result}'
    #change this to 0 to see stdout and stderr
    assert 1
