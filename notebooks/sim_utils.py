import numpy as np
from scipy.integrate import solve_ivp
from typing import Callable, Optional

class Trajectory:
    """Data structure for holding the result of a simulation run"""
    def __init__(self, t: float, X: np.array, u: np.array, params: dict):
        self.t = t
        self.X = X
        self.u = u
        self.params = params

def simulate_entry_trajectory(eom: Callable[[float, np.array], np.array], 
                              t0: float, 
                              tf: float, 
                              X0: np.array, 
                              term_var_idx: int, 
                              term_var_val: float,
                              params: dict,
                              bank_angle_fn: Callable[[float, np.array, dict], float],
                              t_eval: Optional[np.array] = None) -> Trajectory:

    altitude_stop_event = lambda t, X, params, _: X[term_var_idx] - term_var_val
    altitude_stop_event.terminal = True
    altitude_stop_event.direction = -1
    
    output = solve_ivp(eom, 
                   [t0, tf], 
                   X0, 
                   args=(params, bank_angle_fn), 
                   t_eval=t_eval,
                   rtol=1e-6, events=altitude_stop_event)
    
    # loop over output and compute bank angle for each timestep
    num_steps = len(output.t)

    u = np.zeros(num_steps)
    for i, (t, X) in enumerate(zip(output.t, output.y.T)):
        u[i] = bank_angle_fn(t, X, params)
        
    # Transpose y so that each state is in a separate column and each row 
    # represents a timestep
    return Trajectory(output.t, output.y.T, u, params)
