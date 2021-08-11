import numpy as np
from typing import Callable
from numpy import sin, cos, exp

# Fix Python 3's weird rounding function
# https://stackoverflow.com/a/44888699/538379
round2=lambda x,y=None: round(x+1e-15,y)

class ApolloReferenceData:
    def __init__(self, X_and_lam: np.array, u: np.array, tspan: np.array, params: dict):
        """
        X_and_lam: [h, s, v, gam, lamH, lamV, lamGAM, lamU] - 8 x n matrix
        tspan: 1 x n vector
        """
        self.X_and_lam = X_and_lam
        self.tspan = tspan
        self.params = params
        self.u = u

        assert len(X_and_lam.shape) == 2 and X_and_lam.shape[0] > 1, "Need at least two rows of data"
        self.num_rows = X_and_lam.shape[0]
        
        self.delta_v = abs(X_and_lam[1,2] - X_and_lam[0,2])
        assert self.delta_v > 0, "Reference trajectory has repeated velocites in different rows"
        
        self.start_v = X_and_lam[0,2]

        F1, F2, F3, D_m, hdot_ref = self._compute_gains_and_ref()
        F3[-1] = F3[-2]   # Account for F3=0 at t=tf
        # Stack the columns as follows:
        # [t, h, s, v, gam, F1, F2, F3, D/m]
        self.data = np.column_stack((tspan, X_and_lam[:,:4], F1, F2, F3, D_m, hdot_ref))

    def _compute_gains_and_ref(self):
        h = self.X_and_lam[:,0]
        v = self.X_and_lam[:,2]
        gam = self.X_and_lam[:,3]

        lamH = self.X_and_lam[:,4]
        lamGAM = self.X_and_lam[:,6]
        lamU = self.X_and_lam[:,7]
        
        rho0 = self.params['rho0']
        H = self.params['H']
        beta = self.params['beta']   # m/(Cd * Aref)

        v2 = v*v
        rho = rho0 * exp(-h/H) 
        D_m = rho * v2 / (2 * beta)  # Drag Acceleration (D/m)
        hdot = v * sin(gam)
        
        F1 = H * lamH/D_m
        F2 = lamGAM/(v * np.cos(gam))
        F3 = lamU
        return F1, F2, F3, D_m, hdot

    def get_row_by_velocity(self, v: float):
        """
        Returns data row closest to given velocity
        """
        all_v = self.data[:,3]
        dist_to_v = np.abs(all_v - v)
        index = min(dist_to_v) == dist_to_v
        return self.data[index,:][0]
    
    def save(self, filename: str):
        """Saves the reference trajectory data to a file"""
        np.savez(filename, X_and_lam=self.X_and_lam, u=self.u, tspan=self.tspan, params=self.params)

    @staticmethod
    def load(filename: str):
        """Initializes a new ApolloReferenceData from a saved data file"""
        npzdata = np.load(filename, allow_pickle=True)
        X_and_lam = npzdata.get('X_and_lam')
        u = npzdata.get('u')
        tspan = npzdata.get('tspan')
        params = npzdata.get('params').item()
        return ApolloReferenceData(X_and_lam, u, tspan, params)

def traj_eom(t: float, 
             state: np.array, 
             parameters: dict, 
             bank_angle_fn: Callable[[float, np.array, dict], float]
            ):
    h, s, v, gam = state
    u = bank_angle_fn(t, state, parameters)
    
    rho0 = parameters['rho0']
    H = parameters['H']
    beta = parameters['beta']   # m/(Cd * Aref)
    LD = parameters['LD']
    R_m = parameters['R_m']
    g = parameters['g']
    
    v2 = v*v
    rho = rho0 * exp(-h/H) 
    D_m = rho * v2 / (2 * beta)  # Drag Acceleration (D/m)
    r = R_m + h
    return np.array([v * sin(gam),       # dh/dt
                     v * cos(gam),       # ds/dt
                     -D_m - g*sin(gam),  # dV/dt
                     (v2 * cos(gam)/r + D_m*LD*cos(u) - g*cos(gam))/v] # dgam/dt
                   )
