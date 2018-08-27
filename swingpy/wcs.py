from abc import ABC as _ABC
from abc import abstractproperty as _abstractproperty
import numpy as _np
from scipy import signal as _signal


class State(_ABC):
    """
    abstract base class for all leader-follower states

    Working Model
    -------------

                --> x_f   --> r
                |         |
         _______     k
        |       |---/\/---|
        |   m   |         |
        |_______|---[=]---|
                     c

    Equation(s) of Motion: m*x_f'' = - k*x_f - c*x_f'' + k*r
    m: "mass" of follower
    x_f: follower's travel-distance from initial position along slot
    r: travel-distance from initial position of post along slot
    k: "stiffness" in connection
    c: damping coefficient in connection

    State-Space Model: x'' = A*x + B*u
    Output: y = C*x + D*u
    State Variables: x = [x_f, x_f']
    Input: u = [r]
    """

    def __init__(self):
        "system parameters that dictate partner response dynamics"
        self._wn = 2*_np.pi  # natural frequency: wn = sqrt(k/m)
        self._z = 1  # damping ratio: z = c/(2*wn*m)
        self._dt = 0.01  # interval for discrete time step, dt
        self._tau = 2*self.z*self.wn  # time constant: tau = c/k = 2*z/wn

        # State space representation
        A = _np.array([[0, 1], [-self.wn**2, -2*self.z*self.wn]])
        B = _np.array([[0], [self.wn**2]])
        C = _np.array([[1, 0]])
        D = _np.array([[0]])
        self._sys = _signal.lti(A, B, C, D)

    @_abstractproperty
    def state(self):
        pass

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
    def tau(self):
        return self._tau


class OpenPosition(State):
    """
    Contains all patterns that can be performed from open position
    """

    def __init__(self):
        "system parameters that dictate response dynamics of a follower"
        super().__init__()

    def sugarpush(self):
        """returns multiple 1D arrays:
        t: time array
        y: output - response dynamics of follower
        u: input - position of post
        """
        count = 6
        t = _np.arange(0, count, self.dt)  # 6-count
        u = _np.concatenate(
                            (_np.zeros(
                                        int(1/self.dt)),
                                _np.arange(0, 1, self.dt),
                                _np.ones(2*int(1/self.dt)),
                                _np.arange(1, 0, -self.dt),
                                _np.zeros(int(1/self.dt))))
        tout, y, x = _signal.lsim(self._sys, u, t)
        return t, y, u

    @property
    def state(self):
        return self.__class__.__name__


class ClosedPosition(State):
    """
    Contains all patterns that can be performed from closed position
    """
    pass


class StateMachine:
    pass


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    jnj = OpenPosition()
    t, y, u = jnj.sugarpush()

    plt.plot(t, u)
    plt.plot(t, y)
    plt.grid(which='major')
    plt.title('push-break response-dynamics')
    plt.ylabel('travel-distance (w.r.t. initial-conditions)')
    plt.xlabel('count')
    plt.legend(['post', 'follower'])
    plt.show()
