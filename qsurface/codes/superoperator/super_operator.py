from .._template.sim import FaultyMeasurements as BaseFM
import pandas as pd
import random
import numpy as np
from typing import Any, List, Optional, Union, Tuple

class SuperOperator(BaseFM):
    """ Superoperator class to obtain error syndrome in the formalism of superoperator. Superoperator data is obtained via a CSV file which can be generated via other available codes.
    
    Parameters
    ----------
    None

    Object Attributes
    ----------
    stabilizer_type: str
        To categorize the plaquette stabilizer as plaquette and star (vertex) as star type, with 'p' and 's' respectively. Every stabilizer is either 'p' or 's' type.
    
    plaq_rate: float
        The fidelity of the plaquette stabilizer with given error configuration, in the superoperator.
    
    star_rate: float
        The fidelity of the star stabilizer with given error configuration, in the superoperator.
    
    error_config: str 
        The error configuration on the involved data qubits as a string of the {I, X, Y, Z} elements for each qubits in ordered fashion.
    
    measurement_error: bool
        Indicates whether there is a measurement error for the particular stabilizer upon measurement.
    """

    def __init__(self,
        size, *args, layers: Optional[int] = None, p_bitflip_plaq: float = 0, p_bitflip_star: float = 0, **kwargs,):
        """Initializes the superoperator object with default (physically ideal) values."""

        super().__init__(size, *args, layers, p_bitflip_plaq, p_bitflip_star, **kwargs)

        self.stabilizer_type: str = ""
        self.plaq_rate: float = 1.0
        self.star_rate: float = 1.0
        self.error_config: str = ""
        self.measurement_error: bool = False

    def initialize():
        pass



    def csv_to_sup(self, filepath=""):
        """Reads the CSV file for superoperator and returns the pandas dataframe for plaquettes and stars as the output. They contain the fidelity and measurement errors. 
        """

        file_path = filepath
        sup_op_data = pd.read_csv(file_path, sep = ';')

        plaq = sup_op_data.loc[:, ['p', 'error_config', 'lie']]
        star = sup_op_data.loc[:, ['s', 'error_config', 'lie']]

        return plaq, star




    def config_p_s_sup_op(self, plaq, star, stab_type: str = ''):
        """ Calculates and assigns the corresponding fidelity and error configuration for a given superoperator stabilizer type. This function is eventually called for all stabilizers.
        
        Parameters
        ----------
        plaq: pandas.DataFrame
            Pandas dataframe that contains the fidelity and measurement error for each plaquette.

        star: pandas.DataFrame
            Pandas dataframe that contains the fidelity and measurement error for each star.

        stab_type: str
            Takes information on whether we want to implement a plaquette or star type superoperator term for a particular stabilizer.
        """

        self.stabilizer_type = stab_type

        plaq = plaq
        star = star

        """ Extract the fidelities of the corresponding stabilizer types, below."""

        plaq_er = list(plaq.loc[:, 'p'])
        star_er = list(star.loc[:, 's'])

        if self.stabilizer_type == 'p':
            choose = int(random.choices(list(np.arange(len(plaq.index))), weights = plaq_er)[0]) #Choose the index based on fidelity as the weight
            self.measurement_error = bool(list(plaq.iloc[choose])[2]) # Use the above to extract the measurement value as bool out of the above list generated from the row of plaq or star
            self.error_config = str(list(plaq.iloc[choose])[1]) # Similar logic as above to get the error configuration as string

        if self.stabilizer_type == 's':
            choose = int(random.choices(list(np.arange(len(star.index))), weights = star_er)[0])
            self.measurement_error = bool(list(star.iloc[choose])[2])
            self.error_config = str(list(star.iloc[choose])[1])
                            
        return