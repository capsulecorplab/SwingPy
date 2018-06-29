import swingpy as sp
import pytest
from numpy import e

@pytest.fixture
def jill():
    jill = sp.Follower()
    return jill

def test_sugarpush(jill):
    "sugarpush() should return a 1D array for sugar push response dynamics"
    t, y, u = jill.sugarpush()
    assert t[1]-t[0] == jill.dt # has correct time step
    for ti,yi,ui in zip(t,y,u):
        if ti <= 1:
            assert yi == 0
        if ti > 1+jill.tao and ti <= 1.1+jill.tao:
            assert yi > 1-1/e and yi < 1.1-1/e # response has reached 1-1/e of r by time constant
        if ti > 2.5 and ti < 3.5:
            assert yi > 0.9 and yi < 1
        if ti > 4+jill.tao and ti <= 4.1+jill.tao:
            assert yi > 1-1/e and yi < 1.1-1/e # response has reached 1-1/e of r by time constant
        if ti > 5.5:
            assert yi < 0.1

if __name__ == '__main__':
    print(__doc__)
    pytest.main(args=['-v'])
