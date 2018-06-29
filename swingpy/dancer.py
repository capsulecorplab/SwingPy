from math import pi, e
from scipy import signal
import numpy as np

class Follower(object):
    """
                -> x_f  -> r
                |       |
         _______    k
        |       |--/\/--|
        |   m   |       |
        |_______|---D---|
                    c

    Equation(s) of Motion: m*x_f'' = - k*x_f - c*x_f'' + k*r
    m: "mass" of follower
    x_f: follower's position along slot
    r: position of post along slot
    k: "stiffness" in connection
    c: damping coefficient in connection

    State-Space Model: x'' = A*x + B*u
    Output: y = C*x + D*u
    State Variables: x = [x_f, x_f']
    Input: u = [r]
    """

    def __init__(self):
        "response dynamics of follower"
        self._wn = 2*pi # natural frequency: wn = sqrt(k/m)
        self._z = 1 # damping ratio: z = c/(2*wn*m)
        self._dt = 0.01 # interval for discrete time step, dt
        self._tao = 2*self._z*self._wn # time constant: tao = c/k = 2*z/wn

    def sugarpush(self):
        """returns multiple 1D arrays:
        t: time array
        y: output - response dynamics of follower
        u: input - position of post
        """
        count = 6
        sys_tf = signal.lti([self._wn**2],[1, 2*self._z*self._wn, self._wn**2])
        t = np.arange(0, count, self._dt) # 6-count
        u = np.concatenate((np.zeros(int(1/self._dt)),np.arange(0,1,self._dt),np.ones(2*int(1/self._dt)),np.arange(1,0,-self._dt),np.zeros(int(1/self._dt)))) # push-break
        # lowpass = signal.lti([.01],[1, .01])
        tout, y, x = signal.lsim(sys_tf, u, t)
        return t, y, u

    @property
    def wn(self):
        return self._wn

    @property
    def z(self):
        return self._z

    @property
    def dt(self):
        return self._dt

    @property
    def tao(self):
        return self._tao
