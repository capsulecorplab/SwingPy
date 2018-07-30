from scipy import signal
import numpy as np

class Follower(object):
    """
                -> x_f    -> r
                |         |
         _______     k
        |       |---/\/---|
        |   m   |         |
        |_______|---[=]---|
                     c

    Equation(s) of Motion: m*x_f'' = - k*x_f - c*x_f'' + k*r
    m: "mass" of follower
    x_f: follower's deviation from initial position along slot
    r: deviation from initial position of post along slot
    k: "stiffness" in connection
    c: damping coefficient in connection

    State-Space Model: x'' = A*x + B*u
    Output: y = C*x + D*u
    State Variables: x = [x_f, x_f']
    Input: u = [r]
    """

    def __init__(self):
        "system parameters that dictate response dynamics of a follower"
        self._wn = 2*np.pi # natural frequency: wn = sqrt(k/m)
        self._z = 1 # damping ratio: z = c/(2*wn*m)
        self._dt = 0.01 # interval for discrete time step, dt
        self._tau = 2*self._z*self._wn # time constant: tau = c/k = 2*z/wn

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
    def tau(self):
        return self._tau

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    jill = Follower()
    t, y, u = jill.sugarpush()
    plt.plot(t, u)
    plt.plot(t, y)
    plt.grid(which='major')
    plt.title('push-break')
    plt.ylabel('travel distance (w.r.t. initial-conditions)')
    plt.xlabel('count')
    plt.legend(['Post','Follower'])
    plt.show()
