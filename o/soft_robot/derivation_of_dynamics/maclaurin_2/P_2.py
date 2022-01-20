import numpy
def f(q, xi):
    l1, l2, l3 = q[0,0], q[1,0], q[2,0]

    return (0.00625*l1 + 0.00625*l2 + 0.00625*l3 + 0.0028125)*numpy.sqrt(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)*numpy.sin(0.00833333333333333*xi*numpy.sqrt(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2))