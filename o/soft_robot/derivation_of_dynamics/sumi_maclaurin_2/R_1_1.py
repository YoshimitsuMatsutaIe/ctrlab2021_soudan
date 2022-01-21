import numpy
def f(q, xi):
    l1, l2, l3 = q[0,0], q[1,0], q[2,0]

    return 0.5*(l1 - 0.0001)**2*(9.20965520600843e-6*numpy.sqrt(3)*xi**2*1 - 1.16185648486691*numpy.sqrt(3)*xi*0 - 72315.0569809779*numpy.sqrt(3)*(1 - 1)) + 0.5*(l1 - 0.0001)*(l2 - 0.002)*(-1.33958621178304e-5*numpy.sqrt(3)*xi**2*1 - 2.25083125865964*numpy.sqrt(3)*xi*0 - 105605.549121463*numpy.sqrt(3)*(1 - 1)) + 0.5*(l1 - 0.0001)*(l3 - 0.0015)*(-5.02344829418642e-6*numpy.sqrt(3)*xi**2*1 + 4.57454422839345*numpy.sqrt(3)*xi*0 + 250235.663083419*numpy.sqrt(3)*(1 - 1)) + (l1 - 0.0001)*(-0.00114258144640829*numpy.sqrt(3)*xi*0 - 74.8396924930032*numpy.sqrt(3)*(1 - 1)) + 0.5*(l2 - 0.002)**2*(4.87122258830198e-6*numpy.sqrt(3)*xi**2*1 + 2.80662731710959*numpy.sqrt(3)*xi*0 + 271254.509190769*numpy.sqrt(3)*(1 - 1)) + 0.5*(l2 - 0.002)*(l3 - 0.0015)*(3.65341694122649e-6*numpy.sqrt(3)*xi**2*1 - 3.36242337555953*numpy.sqrt(3)*xi*0 - 436903.469260075*numpy.sqrt(3)*(1 - 1)) + (l2 - 0.002)*(0.000830968324660573*numpy.sqrt(3)*xi*0 - 209.551138980409*numpy.sqrt(3)*(1 - 1)) + 0.5*(l3 - 0.0015)**2*(6.85015676479967e-7*numpy.sqrt(3)*xi**2*1 - 0.60606042641696*numpy.sqrt(3)*xi*0 + 93333.9030883277*numpy.sqrt(3)*(1 - 1)) + (l3 - 0.0015)*(0.000311613121747715*numpy.sqrt(3)*xi*0 + 284.390831473412*numpy.sqrt(3)*(1 - 1)) - 0.141752577319588*numpy.sqrt(3)*(1 - 1)