from traceback import print_tb
from ..elements import AncillaQubit, Round
from .._template.sim import PerfectMeasurements as TemplatePM, FaultyMeasurements as TemplateFM
from ...errors.pauli import Sim as Pauli
import random, time
import pandas as pd


class PerfectMeasurements(TemplatePM):
    # Inherited docstring

    name = "weight_3_toric"

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

        # Add cells to the surface
        index = 1
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.add_cell([self.data_qubits[z][(x + 0.5, y)], self.data_qubits[z][(x, y + 0.5)]], z=z, index=index, **kwargs)
                index += 1
        del index
        # The size is even X even for weight-3 architecture

        # Add rounds to the surface, 4 rounds for each X and Z type stabilizer cycles
        ### Add star stabilizer rounds
        round_ancillas_1, round_ancillas_2, round_ancillas_3, round_ancillas_4  = [], [], [], []
        for y in range(0, self.size[1], 2):
            for x in range(0, self.size[0], 2):
                round_ancillas_1.append(self.ancilla_qubits[z][(x, y)])
                round_ancillas_2.append(self.ancilla_qubits[z][(x+1, y)])
                round_ancillas_3.append(self.ancilla_qubits[z][(x+1, y+1)])
                round_ancillas_4.append(self.ancilla_qubits[z][(x, y+1)])
        self.add_round_star(round_ancillas_1, z=z, serial=1, **kwargs)
        self.add_round_star(round_ancillas_2, z=z, serial=2, **kwargs)
        self.add_round_star(round_ancillas_3, z=z, serial=3, **kwargs)
        self.add_round_star(round_ancillas_4, z=z, serial=4, **kwargs)


        ### Add plaq stabilizer rounds
        round_ancillas_1, round_ancillas_2, round_ancillas_3, round_ancillas_4  = [], [], [], []
        for y in range(0, self.size[1], 2):
            for x in range(0, self.size[0], 2):
                round_ancillas_1.append(self.ancilla_qubits[z][(x+0.5, y+0.5)])
                round_ancillas_2.append(self.ancilla_qubits[z][(x+1.5, y+0.5)])
                round_ancillas_3.append(self.ancilla_qubits[z][(x+1.5, y+1.5)])
                round_ancillas_4.append(self.ancilla_qubits[z][(x+0.5, y+1.5)])
        self.add_round_plaq(round_ancillas_1, z=z, serial=1, **kwargs)
        self.add_round_plaq(round_ancillas_2, z=z, serial=2, **kwargs)
        self.add_round_plaq(round_ancillas_3, z=z, serial=3, **kwargs)
        self.add_round_plaq(round_ancillas_4, z=z, serial=4, **kwargs)

        del round_ancillas_1, round_ancillas_2, round_ancillas_3, round_ancillas_4
        

    def init_parity_check(self, ancilla_qubit: AncillaQubit, **kwargs):
        """Initiates a parity check measurement.

        For every ancilla qubit on ``(x,y)``, four neighboring data qubits are entangled for parity check measurements. They are stored via the wind-directional keys.

        Parameters
        ----------
        ancilla_qubit : `~.codes.elements.AncillaQubit`
            Ancilla-qubit to initialize.
        """

        #Boundary conditions are periodic for weight-3 toric code
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
        self.init_superoperator_errors() # Does necessary superoperator initializations on the code, if required!


    def csv_to_sup(self, filepath="NA"):
        """Reads the CSV file for superoperator and stores the CSV data in `self.superoperator_data` and number of entries in ` self.superoperator_size`.
        
        Parameters
        ----------
        filepath
            Relatve/Complete filepath for the superoperator CSV file generated from the circuit simulator
        """
        sup_op_data = pd.read_csv(filepath, sep = ';')
        self.superoperator_data = (sup_op_data.loc[:, ['error_config', 'ghz_success', 'lie', 'p', 's', 'idle']]).to_dict()
        self.superoperator_size = range(len(list(self.superoperator_data['error_config'].keys())))


    """
    ---------------------------------------------------------------------------------------------------------------------
                                    Distributed Superoperator initialization functions
    ---------------------------------------------------------------------------------------------------------------------
    """

    def init_superoperator_errors(self, *args, **kwargs):
        """Initializes required parameters from `self.superoperator_data`."""
        return

    """
    ---------------------------------------------------------------------------------------------------------------------
                                    Distributed Superoperator application functions
    ---------------------------------------------------------------------------------------------------------------------
    """

    def round_noise(self, ancilla: AncillaQubit):
        "Applies noisy superoperator on the current round data and ancilla qubits via each stabilizer ancilla qubit."
        if ancilla.state_type == 'x':
            choose = random.choices(self.superoperator_errors, weights = self.superoperator_data['s'].values())[0] #Choose the index based on fidelity as the weight
            measurement_error = self.superoperator_data['lie'][choose] # Use the above to extract the measurement value as bool out of the above list generated from the row of plaq or star
            error_config = self.superoperator_data['error_config'][choose] # Similar logic as above to get the error configuration as string
            ghz_success = self.superoperator_data['ghz_success'][choose]

            ancilla.super_error = measurement_error
            ancilla.ghz_success = ghz_success

            _pauli = Pauli
            for serial, data_qubit in zip(range(4), ancilla.parity_qubits.values()):
                if error_config[serial] == 'X':
                    _pauli.bitflip(data_qubit)
                elif error_config[serial] == 'Z':
                    _pauli.phaseflip(data_qubit)
                elif error_config[serial] == 'Y':
                    _pauli.bitphaseflip(data_qubit)

        if ancilla.state_type == 'z':
            choose = random.choices(self.superoperator_errors, weights = self.superoperator_data['p'].values())[0] #Choose the index based on fidelity as the weight
            measurement_error = self.superoperator_data['lie'][choose] # Use the above to extract the measurement value as bool out of the above list generated from the row of plaq or star
            error_config = self.superoperator_data['error_config'][choose] # Similar logic as above to get the error configuration as string
            ghz_success = self.superoperator_data['ghz_success'][choose]

            ancilla.super_error = measurement_error
            ancilla.ghz_success = ghz_success

            _pauli = Pauli
            for serial, data_qubit in zip(range(4), ancilla.parity_qubits.values()):
                if error_config[serial] == 'X':
                    _pauli.bitflip(data_qubit)
                elif error_config[serial] == 'Z':
                    _pauli.phaseflip(data_qubit)
                elif error_config[serial] == 'Y':
                    _pauli.bitphaseflip(data_qubit)
        return


    def qubit_idling(self, ancilla: AncillaQubit):
        "Applies idling superoperator on the current round data and ancilla qubits via each stabilizer ancilla qubit."
        choose = random.choices(self.superoperator_errors, weights = self.superoperator_data['idle'].values())[0] #Choose the index based on fidelity as the weight
        error_config = self.superoperator_data['error_config'][choose]

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
                                    Distributed Superoperator simulation functions
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

            # Star sequence starts here
            self.superoperator_apply_round(self.rounds_star[self.layer][1])
            self.superoperator_apply_idling(self.rounds_star[self.layer][3])
            self.superoperator_measure_round(self.rounds_star[self.layer][1])

            self.superoperator_apply_round(self.rounds_star[self.layer][2])
            self.superoperator_apply_idling(self.rounds_star[self.layer][4])
            self.superoperator_measure_round(self.rounds_star[self.layer][2])

            self.superoperator_apply_round(self.rounds_star[self.layer][3])
            self.superoperator_apply_idling(self.rounds_star[self.layer][1])
            self.superoperator_measure_round(self.rounds_star[self.layer][3])

            self.superoperator_apply_round(self.rounds_star[self.layer][4])
            self.superoperator_apply_idling(self.rounds_star[self.layer][2])
            self.superoperator_measure_round(self.rounds_star[self.layer][4])
            # Star sequence ends here

            # Plaquette sequence starts here
            self.superoperator_apply_round(self.rounds_plaq[self.layer][1])
            self.superoperator_apply_idling(self.rounds_plaq[self.layer][3])
            self.superoperator_measure_round(self.rounds_plaq[self.layer][1])

            self.superoperator_apply_round(self.rounds_plaq[self.layer][2])
            self.superoperator_apply_idling(self.rounds_plaq[self.layer][4])
            self.superoperator_measure_round(self.rounds_plaq[self.layer][2])

            self.superoperator_apply_round(self.rounds_plaq[self.layer][3])
            self.superoperator_apply_idling(self.rounds_plaq[self.layer][1])
            self.superoperator_measure_round(self.rounds_plaq[self.layer][3])

            self.superoperator_apply_round(self.rounds_plaq[self.layer][4])
            self.superoperator_apply_idling(self.rounds_plaq[self.layer][2])
            self.superoperator_measure_round(self.rounds_plaq[self.layer][4])
            # Plaquette sequence ends here


            # self.superoperator_random_measure_layer()
        # Now measure the layer to get the syndrome after all the rounds of current cycle are finished
        self.layer = self.layers - 1
        self.superoperator_random_measure_layer(ideal_measure=True) # Last layer perfect measurements with no round and idling noise.
        return
        

    def superoperator_apply_round(self, round: Round):
        """ Applies the round noise to all ancillas in a particular round. """
        for round_ancilla in round.round_ancillas:
            self.round_noise(round_ancilla)
        return

    def superoperator_apply_idling(self, round: Round):
        """ Applies the idle noise to all ancillas in a particular round. """
        for idle_ancilla in round.round_ancillas:
            self.qubit_idling(idle_ancilla)

        # for ancilla in self.ancilla_qubits[self.layer].values(): 
        #         ancilla.measure(0, 0, False)
        return

    def superoperator_measure_round(self, round: Round, ideal_measure = False):
        """ Applies the round noise to all ancillas in a particular round. """
        for round_ancilla in round.round_ancillas:
            previous_ancilla = self.ancilla_qubits[(round_ancilla.z - 1) % self.layers][round_ancilla.loc]
            if round_ancilla.ghz_success == False:
                round_ancilla.measured_state = previous_ancilla.measured_state
                round_ancilla.syndrome = False
            else:
                if ideal_measure:
                    measured_state = round_ancilla.measure(ideal_measure=True)
                else:
                    measured_state = round_ancilla.measure()
                round_ancilla.syndrome = measured_state != previous_ancilla.measured_state
        return

    def superoperator_random_measure_layer(self, ideal_measure = False):
        """ Measures a layer of ancillas. If ideal measure is True, then measure ideally, else measure faulty by default.

        If the measured state of the current ancilla is not equal to the measured state of the previous instance, the current ancilla is a syndrome."""
        for ancilla in self.ancilla_qubits[self.layer].values():
            previous_ancilla = self.ancilla_qubits[(ancilla.z - 1) % self.layers][ancilla.loc]
            if ideal_measure:
                measured_state = ancilla.measure(ideal_measure=True)
                ancilla.syndrome = measured_state != previous_ancilla.measured_state
            else:
                if ancilla.ghz_success == False:
                    ancilla.syndrome = previous_ancilla.syndrome
                measured_state = ancilla.measure()
                ancilla.syndrome = measured_state != previous_ancilla.measured_state
        return