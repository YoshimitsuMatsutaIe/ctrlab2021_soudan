import numpy
def f(q, q_dot, xi):
    return numpy.array([[-12828156665.2727*xi**10*(2*l1 - l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4 + 2004399.47894886*xi**8*(2*l1 - l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3 - 7990976.98521566*xi**6*(2*l1 - l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2 + 84279.8353909465*xi**4*(2*l1 - l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2) - 355.555555555555*xi**2*(2*l1 - l2 - l3)**2 + 1, 12828156665.2727*numpy.sqrt(3)*xi**10*(l2 - l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4 + 405890894.487145*numpy.sqrt(3)*xi**8*(l2 - l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3 - 7990976.98521566*numpy.sqrt(3)*xi**6*(l2 - l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2 + 84279.8353909465*numpy.sqrt(3)*xi**4*(l2 - l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2) - 355.555555555555*numpy.sqrt(3)*xi**2*(l2 - l3)*(2*l1 - l2 - l3), -2405279374.73864*xi**9*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4 + 30441817.0865359*xi**7*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3 - 898984.910836762*xi**5*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2 + 6320.98765432099*xi**3*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2) - 26.6666666666667*xi*(2*l1 - l2 - l3)], [12828156665.2727*numpy.sqrt(3)*xi**10*(l2 - l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4 + 405890894.487145*numpy.sqrt(3)*xi**8*(l2 - l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3 - 7990976.98521566*numpy.sqrt(3)*xi**6*(l2 - l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2 + 84279.8353909465*numpy.sqrt(3)*xi**4*(l2 - l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2) - 355.555555555555*numpy.sqrt(3)*xi**2*(l2 - l3)*(2*l1 - l2 - l3), -38484469995.8182*xi**10*(l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4 + 1217672683.46143*xi**8*(l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3 - 23972930.955647*xi**6*(l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2 + 252839.506172839*xi**4*(l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2) - 1066.66666666667*xi**2*(l2 - l3)**2 + 1, -4810558749.47727*numpy.sqrt(3)*xi**9*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4 + 121767268.346143*numpy.sqrt(3)*xi**7*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3 - 1797969.82167352*numpy.sqrt(3)*xi**5*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2 + 12641.975308642*numpy.sqrt(3)*xi**3*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2) - 26.6666666666667*numpy.sqrt(3)*xi*(l2 - l3)], [2405279374.73864*xi**9*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4 - 30441817.0865359*xi**7*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3 + 898984.910836762*xi**5*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2 - 6320.98765432099*xi**3*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2) + 26.6666666666667*xi*(2*l1 - l2 - l3), 4810558749.47727*numpy.sqrt(3)*xi**9*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4 - 121767268.346143*numpy.sqrt(3)*xi**7*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3 + 1797969.82167352*numpy.sqrt(3)*xi**5*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2 - 12641.975308642*numpy.sqrt(3)*xi**3*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2) + 26.6666666666667*numpy.sqrt(3)*xi*(l2 - l3), -51312626661.0909*xi**10*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**5 + 1623563577.94858*xi**8*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4 - 31963907.9408627*xi**6*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3 + 337119.341563786*xi**4*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2 - 1422.22222222222*xi**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2) + 1]])