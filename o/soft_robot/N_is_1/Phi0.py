import numpy

def f(q_large, xi_large, q_dot_large):
    return numpy.array([[-160351958.315909*(2*q_large[0, 0] - q_large[1, 0] - q_large[2, 0])*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*(q_large[0, 0]**2 - q_large[0, 0]*q_large[1, 0] - q_large[0, 0]*q_large[2, 0] + q_large[1, 0]**2 - q_large[1, 0]*q_large[2, 0] + q_large[2, 0]**2)**4*xi_large[0, 0]**10 + 5073636.18108931*(2*q_large[0, 0] - q_large[1, 0] - q_large[2, 0])*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*(q_large[0, 0]**2 - q_large[0, 0]*q_large[1, 0] - q_large[0, 0]*q_large[2, 0] + q_large[1, 0]**2 - q_large[1, 0]*q_large[2, 0] + q_large[2, 0]**2)**3*xi_large[0, 0]**8 - 99887.2123151958*(2*q_large[0, 0] - q_large[1, 0] - q_large[2, 0])*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*(q_large[0, 0]**2 - q_large[0, 0]*q_large[1, 0] - q_large[0, 0]*q_large[2, 0] + q_large[1, 0]**2 - q_large[1, 0]*q_large[2, 0] + q_large[2, 0]**2)**2*xi_large[0, 0]**6 + 1053.49794238683*(2*q_large[0, 0] - q_large[1, 0] - q_large[2, 0])*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*(q_large[0, 0]**2 - q_large[0, 0]*q_large[1, 0] - q_large[0, 0]*q_large[2, 0] + q_large[1, 0]**2 - q_large[1, 0]*q_large[2, 0] + q_large[2, 0]**2)*xi_large[0, 0]**4 - 4.44444444444444*(2*q_large[0, 0] - q_large[1, 0] - q_large[2, 0])*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*xi_large[0, 0]**2], [-160351958.315909*numpy.sqrt(3)*(q_large[1, 0] - q_large[2, 0])*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*(q_large[0, 0]**2 - q_large[0, 0]*q_large[1, 0] - q_large[0, 0]*q_large[2, 0] + q_large[1, 0]**2 - q_large[1, 0]*q_large[2, 0] + q_large[2, 0]**2)**4*xi_large[0, 0]**10 + 5073636.18108931*numpy.sqrt(3)*(q_large[1, 0] - q_large[2, 0])*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*(q_large[0, 0]**2 - q_large[0, 0]*q_large[1, 0] - q_large[0, 0]*q_large[2, 0] + q_large[1, 0]**2 - q_large[1, 0]*q_large[2, 0] + q_large[2, 0]**2)**3*xi_large[0, 0]**8 - 99887.2123151958*numpy.sqrt(3)*(q_large[1, 0] - q_large[2, 0])*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*(q_large[0, 0]**2 - q_large[0, 0]*q_large[1, 0] - q_large[0, 0]*q_large[2, 0] + q_large[1, 0]**2 - q_large[1, 0]*q_large[2, 0] + q_large[2, 0]**2)**2*xi_large[0, 0]**6 - 4.44444444444444*numpy.sqrt(3)*(q_large[1, 0] - q_large[2, 0])*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*xi_large[0, 0]**2 + 1053.49794238683*numpy.sqrt(3)*(2*q_large[0, 0] - q_large[1, 0] - q_large[2, 0])*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*(q_large[0, 0]**2 - q_large[0, 0]*q_large[1, 0] - q_large[0, 0]*q_large[2, 0] + q_large[1, 0]**2 - q_large[1, 0]*q_large[2, 0] + q_large[2, 0]**2)*xi_large[0, 0]**4], [60131984.3684659*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*(q_large[0, 0]**2 - q_large[0, 0]*q_large[1, 0] - q_large[0, 0]*q_large[2, 0] + q_large[1, 0]**2 - q_large[1, 0]*q_large[2, 0] + q_large[2, 0]**2)**4*xi_large[0, 0]**9 - 1522090.85432679*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*(q_large[0, 0]**2 - q_large[0, 0]*q_large[1, 0] - q_large[0, 0]*q_large[2, 0] + q_large[1, 0]**2 - q_large[1, 0]*q_large[2, 0] + q_large[2, 0]**2)**3*xi_large[0, 0]**7 + 22474.6227709191*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*(q_large[0, 0]**2 - q_large[0, 0]*q_large[1, 0] - q_large[0, 0]*q_large[2, 0] + q_large[1, 0]**2 - q_large[1, 0]*q_large[2, 0] + q_large[2, 0]**2)**2*xi_large[0, 0]**5 - 79.0123456790123*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*(2*q_large[0, 0]**2 - 2*q_large[0, 0]*q_large[1, 0] - 2*q_large[0, 0]*q_large[2, 0] + 2*q_large[1, 0]**2 - 2*q_large[1, 0]*q_large[2, 0] + 2*q_large[2, 0]**2)*xi_large[0, 0]**3 + (1/3)*(q_large[0, 0] + q_large[1, 0] + q_large[2, 0] + 0.45)*xi_large[0, 0]]])