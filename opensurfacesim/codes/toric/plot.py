from .sim import PerfectMeasurements as SimPM, FaultyMeasurements as SimFM
from .._template.plot import PerfectMeasurements as TemplatePM


class PerfectMeasurements(SimPM, TemplatePM):
    """Plotting toric code class for perfect measurements."""

    class Figure(TemplatePM.Figure):
        """Toric code plot for perfect measurements."""

        def __init__(self, code, *args, **kwargs) -> None:
            self.main_boundary = [-0.25, -0.25, code.size[0] + 0.5, code.size[1] + 0.5]
            super().__init__(code, *args, **kwargs)

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
