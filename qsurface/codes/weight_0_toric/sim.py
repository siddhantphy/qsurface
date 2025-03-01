from ..elements import AncillaQubit, Round
from .._template.sim import PerfectMeasurements as TemplatePM, FaultyMeasurements as TemplateFM
from ...errors.pauli import Sim as Pauli
import random, time
import pandas as pd


class PerfectMeasurements(TemplatePM):
    # Inherited docstring

    name = "weight_0_toric"

    def init_surface(self, z: float = 0, **kwargs):
        """Initializes the toric surface code on layer ``z``.

        Parameters
        ----------
        z : int or float, optional
            Layer of qubits, ``z=0`` for perfect measurements.
        """
        self.ancilla_qubits[z], self.data_qubits[z] = {}, {}
        self.cells[z] = {}
        self.rounds_plaq[z], self.rounds_star[z] = {}, {}

        # Add data qubits to surface
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.add_data_qubit((x + 0.5, y), z=z, **kwargs)
                self.add_data_qubit((x, y + 0.5), z=z, **kwargs)

        # Add ancilla qubits to surface
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                star = self.add_ancilla_qubit((x, y), z=z, state_type="x", **kwargs)
                self.init_parity_check(star)

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                plaq = self.add_ancilla_qubit((x + 0.5, y + 0.5), z=z, state_type="z", **kwargs)
                self.init_parity_check(plaq)


    def init_parity_check(self, ancilla_qubit: AncillaQubit, **kwargs):
        """Initiates a parity check measurement.

        For every ancilla qubit on ``(x,y)``, four neighboring data qubits are entangled for parity check measurements. They are stored via the wind-directional keys.

        Parameters
        ----------
        ancilla_qubit : `~.codes.elements.AncillaQubit`
            Ancilla-qubit to initialize.
        """

        #Boundary conditions are periodic for weight-4 toric code
        (x, y), z = ancilla_qubit.loc, ancilla_qubit.z
        checks = {
            (0.5, 0): ((x + 0.5) % self.size[0], y),
            (-0.5, 0): ((x - 0.5) % self.size[0], y),
            (0, 0.5): (x, (y + 0.5) % self.size[1]),
            (0, -0.5): (x, (y - 0.5) % self.size[1]),
        }
        for key, loc in checks.items():
            if loc in self.data_qubits[z]:
                self.entangle_pair(self.data_qubits[z][loc], ancilla_qubit, key)

    def init_logical_operator(self, **kwargs):
        """Initiates the logical operators [x1, x2, z1, z2] of the toric code."""
        operators = {
            "x1": [self.data_qubits[self.decode_layer][(i, 0.5)].edges["x"] for i in range(self.size[0])],
            "x2": [self.data_qubits[self.decode_layer][(0.5, i)].edges["x"] for i in range(self.size[1])],
            "z1": [self.data_qubits[self.decode_layer][(i + 0.5, 0)].edges["z"] for i in range(self.size[0])],
            "z2": [self.data_qubits[self.decode_layer][(0, i + 0.5)].edges["z"] for i in range(self.size[1])],
        }
        self.logical_operators = operators

    @staticmethod
    def _parse_boundary_coordinates(size, *args):
        # Inherited docstrings
        options = {-1: [*args]}
        for i, arg in enumerate(args):
            if arg == 0:
                options[i] = [*args]
                options[i][i] = size
        diff = {
            option: sum([abs(args[i] - args[j]) for i in range(len(args)) for j in range(i + 1, len(args))])
            for option, args in options.items()
        }
        return options[min(diff, key=diff.get)]

    

class FaultyMeasurements(TemplateFM, PerfectMeasurements):
    # Inherited docstring

    def initialize(self, sup_file = "NA", *args, **kwargs):
        """Initializes all data objects of the code.

        Builds the surface with `init_surface`, adds the logical operators with `init_logical_operator`, and loads error modules with `init_errors`. All keyword arguments from these methods can be used for `initialize`.
        """
        if sup_file != "NA":
            self.superoperator_enabled = True

        self.init_surface(**kwargs)
        self.init_logical_operator(**kwargs)
        self.csv_to_sup(filepath=sup_file)
        self.init_superoperator_errors() # loads fresh errors and measurements from the superoperator_data dictionary


    def csv_to_sup(self, filepath="NA"):
        """Reads the CSV file for superoperator and stores the CSV data in `self.superoperator_data` and number of entries in ` self.superoperator_size`.
        
        Parameters
        ----------
        filepath
            Relatve/Complete filepath for the superoperator CSV file generated from the circuit simulator
        """
        sup_op_data = pd.read_csv(filepath, sep = ';')
        self.superoperator_data = (sup_op_data.loc[:, ['error_config', 'lie', 'p', 's']]).to_dict()
        self.superoperator_size = list(range(len(list(self.superoperator_data['error_config'].keys()))))


    """
    ---------------------------------------------------------------------------------------------------------------------
                                         Superoperator initialization functions
    ---------------------------------------------------------------------------------------------------------------------
    """

    def init_superoperator_errors(self, *args, **kwargs):
        """Initializes required parameters from `self.superoperator_data`."""
        return

    """
    ---------------------------------------------------------------------------------------------------------------------
                                         Superoperator application functions
    ---------------------------------------------------------------------------------------------------------------------
    """

    def qubit_noise(self, ancilla: AncillaQubit):
        "Applies noisy superoperator on the current round data and ancilla qubits via each stabilizer ancilla qubit."
        if ancilla.state_type == 'x':
            stab_type = 's'
        if ancilla.state_type == 'z':
            stab_type = 'p'

        choose = random.choices(self.superoperator_size, weights = self.superoperator_data[f'{stab_type}'].values())[0] #Choose the index based on fidelity as the weight
        measurement_error = self.superoperator_data['lie'][choose] # Use the above to extract the measurement value as bool out of the above list generated from the row of plaq or star
        error_config = self.superoperator_data['error_config'][choose] # Similar logic as above to get the error configuration as string

        ancilla.super_error = measurement_error

        _pauli = Pauli
        for serial, data_qubit in zip(range(4), ancilla.parity_qubits.values()):
            if error_config[serial] == 'X':
                _pauli.bitflip(data_qubit)
            elif error_config[serial] == 'Z':
                _pauli.phaseflip(data_qubit)
            elif error_config[serial] == 'Y':
                _pauli.bitphaseflip(data_qubit)
        return


    """
    ---------------------------------------------------------------------------------------------------------------------
                                        Superoperator simulation functions
    ---------------------------------------------------------------------------------------------------------------------
    """

    def superoperator_random_errors(self):
        """Performs the main simulation by performing noisy stabilizer rounds and measurement for each layer and iteration."""
        self.instance = time.time()

        for ancilla in self.ancilla_qubits[self.layers - 1].values():
            ancilla.measured_state = False

        for z in range(self.layers - 1):
            self.layer = z

            for data in self.data_qubits[self.layer].values():
                data.state = self.data_qubits[(self.layer - 1) % self.layers][data.loc].state

            self.superoperator_apply_noise_layer()
            self.superoperator_random_measure_layer()
            
        self.layer = self.layers - 1 # The last layer
        for data in self.data_qubits[self.layer].values():
                data.state = self.data_qubits[(self.layer - 1) % self.layers][data.loc].state
        
        self.superoperator_apply_noise_layer()

        for ancilla in self.ancilla_qubits[self.layers - 1].values():
            ancilla.super_error = False # reset the errors imposed by the noise layer

        self.superoperator_random_measure_layer(ideal_measure=True) # Last layer perfect measurements

        return
        

    def superoperator_apply_noise_layer(self):
        """ Applies the noise to all ancillas in a particular layer. """
        for ancilla in self.ancilla_qubits[self.layer].values():
            self.qubit_noise(ancilla)
        return


    def superoperator_random_measure_layer(self, ideal_measure = False):
        """ Measures a layer of ancillas. If ideal measure is True, then measure ideally, else measure faulty by default.

        If the measured state of the current ancilla is not equal to the measured state of the previous instance, the current ancilla is a syndrome."""
        for ancilla in self.ancilla_qubits[self.layer].values():
            previous_ancilla = self.ancilla_qubits[(ancilla.z - 1) % self.layers][ancilla.loc]
            measured_state = ancilla.measure(p_bitflip_plaq=0, p_bitflip_star=0,ideal_measure=ideal_measure)
            ancilla.syndrome = measured_state != previous_ancilla.measured_state
        return