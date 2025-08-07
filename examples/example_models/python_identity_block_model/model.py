from pythonfmu.fmi2slave import Fmi2Slave
from pythonfmu.variables import Real
from pythonfmu.enums import Fmi2Causality, Fmi2Variability

class IdentityModel(Fmi2Slave):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize and register variables
        self.input_value = 0.0
        self.register_variable(Real(
            "input_value", 
            causality=Fmi2Causality.input,
            variability=Fmi2Variability.continuous,
            getter=lambda: self.input_value,
            setter=lambda v: setattr(self, "input_value", v)
        ))
        
        self.output_value = 0.0
        self.register_variable(Real(
            "output_value",
            causality=Fmi2Causality.output,
            variability=Fmi2Variability.continuous,
            getter=lambda: self.output_value
        ))
        
        self.test_param = 20.0
        self.register_variable(Real(
            "test_param",
            causality=Fmi2Causality.parameter,
            variability=Fmi2Variability.fixed,
            getter=lambda: self.test_param,
            setter=lambda v: setattr(self, "test_param", v),
            start=20.0
        ))

    def do_step(self, current_time, step_size):
        self.output_value = self.input_value * self.test_param
        return True