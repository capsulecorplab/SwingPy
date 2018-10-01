from swingpy import wcs
import pytest
from numpy import pi, e


@pytest.fixture()
def jnj():
    jnj = wcs.OpenPosition()
    return jnj


def test_system_parameters(jnj):
    assert jnj.state == 'OpenPosition'
    assert jnj.wn == 2*pi
    assert jnj.z == 0.7
    assert jnj.dt == 0.01
    assert jnj.tau == 2*0.7*2*pi


def test_sugarpush(jnj):
    "sugarpush() should return a 1D array for sugar push response dynamics"
    t, y, u = jnj.sugarpush()
    assert t[1]-t[0] == jnj.dt  # has correct time step
    for ti, yi, ui in zip(t, y, u):
        if ti <= 1:
            assert yi == 0
        if ti > 1+jnj.tau and ti <= 1.1+jnj.tau:
            # response has reached 1-1/e of r by time constant
            assert yi > 1-1/e and yi < 1.1-1/e
        if ti > 2.5 and ti < 3.5:
            assert yi > 0.9 and yi < 1.1
        if ti > 4+jnj.tau and ti <= 4.1+jnj.tau:
            # response has reached 1-1/e of r by time constant
            assert yi > 1-1/e and yi < 1.1-1/e
        if ti > 5.5:
            assert yi < 0.1

if __name__ == '__main__':
    print(__doc__)
    pytest.main(args=['-v'])
