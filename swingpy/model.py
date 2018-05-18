# Differential equation：　x'' = ax' + bx
# Turn into 1st order differential equation：　x2' = a*x2 + b*x1; x1=x, x2=x', x2=x1'
# State：　[x1', x2'] = [[0,1], [a,b]] * [x1, x2]
# Output：　y = [1,0]*[x1, x2]

class Dancer(object):
    def __init__(self):
        """dancer's initial conditions for translational dynamics"""
        self.x = 0
        self.x_dot = 0
        """dancer's initial conditions for rotational dynamics"""
        self.theta = 0
        self.theta_dot = 0

    def state(self):
        """return state of dancer for given input"""
        pass
