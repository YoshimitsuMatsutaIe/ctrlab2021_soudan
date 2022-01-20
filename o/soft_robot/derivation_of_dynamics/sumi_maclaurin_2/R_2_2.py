import numpy
def f(q, xi):
    l1, l2, l3 = q[0,0], q[1,0], q[2,0]

    return 0.5*(l1 - 0.0001)**2*(-6.28419795524558e-5*xi**2*0 + 0.913354235306622*xi*1 - 64250.1281954051*0) + 0.5*(l1 - 0.0001)*(l2 - 0.002)*(9.1406515712663e-5*xi**2*0 + 2.96701739469302*xi*1 - 208715.567955983*0) + 0.5*(l1 - 0.0001)*(l3 - 0.0015)*(3.42774433922486e-5*xi**2*0 - 4.79372586530627*xi*1 + 337215.824346793*0) + (l1 - 0.0001)*(-0.00779639175257732*xi*1 - 37.7712874845715*0) + 0.5*(l2 - 0.002)**2*(-3.32387329864229e-5*xi**2*0 + 1.14695150033656*xi*1 - 80682.5852247754*0) + 0.5*(l2 - 0.002)*(l3 - 0.0015)*(-2.49290497398172e-5*xi**2*0 - 5.26092039536614*xi*1 + 370080.738405533*0) + (l2 - 0.002)*(0.00567010309278351*xi*1 - 105.7596049568*0) + 0.5*(l3 - 0.0015)**2*(-4.67419682621572e-6*xi**2*0 + 5.0273231303362*xi*1 - 353648.281376163*0) + (l3 - 0.0015)*(0.00212628865979382*xi*1 + 143.530892441372*0) + 0.967247129904906*0