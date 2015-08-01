import pytest

import cubature._test_integrands as ti
from cubature import cubature
import numpy as np

# test that the Genz oscillatory exact formula actually agrees at an 
# even and odd dimension
def test_genz_oscillatory_exact_d3():
    exact = 4 * np.cos(1056 + np.pi/7)*np.sin(12)*np.sin(306)*np.sin(738)/6273
    calculated = ti.genz_oscillatory_exact(12, np.array([2, 123, 51]), 1/14)
    assert np.allclose([exact], [calculated])

def test_genz_oscillatory_exact_d4():
    exact = np.sin(29988 - 7*np.pi/34) * \
            np.sin(51)*np.sin(2601/2)*np.sin(6273/2)*np.sin(25500) / \
            784125
    calculated = ti.genz_oscillatory_exact(51, np.array([2, 123, 51, 1000]),
            11/17)
    assert np.allclose([exact], [calculated])

def test_genz_oscillatory_d2():
    x = np.array([17, 201], dtype=float)
    a = np.array([41, 1/11], dtype=float)
    u = 1/51

    exact = np.cos(7868/11 + 2*np.pi/51)
    calculated = ti.genz_oscillatory(x, a, u)
    assert np.allclose([exact], [calculated])

def test_genz_oscillatory_c_d2():
    x = np.array([17, 201], dtype=float)
    a = np.array([41, 1/11], dtype=float)
    u = 1/51

    exact = np.cos(7868/11 + 2*np.pi/51)
    calculated = ti.genz_oscillatory(x, a, u)
    calculated_2 = ti.genz_oscillatory_c(x, a, u)

    assert np.allclose([exact], [calculated_2])
    assert np.allclose([calculated], [calculated_2])

def test_hcubature_genz_oscillatory_d2():
    u = 2*np.pi*15/609
    a = np.array([15.51, 2], dtype=float)
    n = 3

    xmin = np.zeros((2,))
    xmax = np.ones((2,)) * n

    exact = ti.genz_oscillatory_exact(n, a, u)

    # check that integrand is callable
    ti.genz_oscillatory(np.ones((2,), dtype=float), a, u)
    
    val, err = cubature(ti.genz_oscillatory, 2, 1, xmin, xmax, args=(a, u),
            adaptive='h')
    assert np.allclose(exact, val) 

def test_cubature_zero_exact():
    d = 1
    xmin = np.zeros((d,), dtype=float)
    xmax = np.ones((d,), dtype=float)*np.pi/2
    
    assert np.allclose(0., ti.cubature_zero_exact(xmin))
    assert np.allclose(1., ti.cubature_zero_exact(xmax))

    d = 3
    xmin = np.zeros((d,), dtype=float)
    assert np.allclose(0., ti.cubature_zero_exact(xmin))
    assert np.allclose(1., ti.cubature_zero_exact(xmax))

    d = 4
    xmin = np.zeros((d,), dtype=float)
    assert np.allclose(0., ti.cubature_zero_exact(xmin))
    assert np.allclose(1., ti.cubature_zero_exact(xmax))

def test_cubature_zero():
    d = 5
    k = 2/np.sqrt(np.pi)
    x = np.ones((d,), dtype=float)
    expected = k**d 
    assert np.allclose(ti.cubature_one(x), expected)


def test_hcubature_cubature_zero():
    xmin = np.zeros((4,))
    xmax = np.array([12, 4, 0.25, 1], dtype=float)

    # check that it is possible to run
    ti.cubature_zero(xmax)

    exact = ti.cubature_zero_exact(xmax)
    val, err = cubature(ti.cubature_zero, xmax.shape[0], 1, xmin, xmax)

    assert np.allclose([exact], [val])

def test_hcubature_cubature_one():
    d = 3
    xmax = np.ones((d,), dtype=float)
    xmin = np.zeros_like(xmax)

    ti.cubature_one(xmin)
    exact = ti.cubature_one_exact(xmax)
    val, err = cubature(ti.cubature_one, d, 1, xmin, xmax)
    assert np.allclose([exact], [val])

def test_cubature_two_exact():
    radius = 1.

    d = 1
    exact = 2
    val = ti.cubature_two_exact(d, radius)
    assert np.allclose([exact], [val])

    d = 2
    exact = np.pi
    val = ti.cubature_two_exact(d, radius)
    assert np.allclose([exact], [val])

    d = 3
    exact = 4/3*np.pi
    val = ti.cubature_two_exact(d, radius)
    assert np.allclose([exact], [val])

@pytest.mark.slow
def test_hcubature_cubature_two():
    radius = 0.68244456511919859846 
    d = 2
    xmin = -np.ones((d,))
    xmax = np.ones((d,))

    exact = ti.cubature_two_exact(d, radius)

    val, err = cubature(ti.cubature_two, d, 1, xmin, xmax, args=(radius,),
            abserr=1e-4, relerr=1e-4, maxEval=1000000)
    true_error = np.abs(val - exact)
    assert true_error < 1e-4
