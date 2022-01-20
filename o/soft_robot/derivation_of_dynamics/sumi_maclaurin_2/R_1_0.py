import numpy
def f(q, xi):
    l1, l2, l3 = q[0,0], q[1,0], q[2,0]

    return 0.5*(l1 - 0.0001)**2*(-6.07837243596557e-5*xi**2*1 - 1.4723987711447*xi*0 - 121438.163869571*1 + 121438.163869571) + 0.5*(l1 - 0.0001)*(l2 - 0.002)*(8.8412689977681e-5*xi**2*1 - 4.09059149510746*xi*0 - 387780.362371481*1 + 387780.362371481) + 0.5*(l1 - 0.0001)*(l3 - 0.0015)*(3.31547587416304e-5*xi**2*1 + 7.03538903739686*xi*0 + 630656.690110624*1 - 630656.690110624) + (l1 - 0.0001)*(0.00754103754629469*xi*0 - 73.0683388245297*1 + 73.0683388245297) + 0.5*(l2 - 0.002)**2*(-3.21500690827931e-5*xi**2*1 + 0.0899501794735671*xi*0 - 133709.809902707*1 + 133709.809902707) + 0.5*(l2 - 0.002)*(l3 - 0.0015)*(-2.41125518120948e-5*xi**2*1 + 3.91069113616032*xi*0 + 655199.982176895*1 - 655199.982176895) + (l2 - 0.002)*(-0.00548439094275978*xi*0 - 204.591348708683*1 + 204.591348708683) + 0.5*(l3 - 0.0015)**2*(-4.52110346476778e-6*xi**2*1 - 5.47304008677859*xi*0 - 642928.33614376*1 + 642928.336143759) + (l3 - 0.0015)*(-0.00205664660353492*xi*0 + 277.659687533213*1 - 277.659687533213) + 0.935567010309278*1 + 0.0644329896907217