import numpy as np
from math import sin, cos, sqrt
import matplotlib.pyplot as plt
import sympy
import scipy
import scipy.optimize
from scipy.optimize import fsolve
from scipy.integrate import odeint


T = np.arange(0.0, 5.2, 0.1)
T1 = np.arange(0.0, 5.1, 0.1)
T2 = np.arange(0.0, 5.0, 0.1)

#qdを求める
def calc_qd(p, t):

    """参照軌道qdを求める"""
    
    l1,l2,l3=p[0],p[1],p[2]
    f=np.zeros(3)
    f[0]=2106.99588477366*l1**4 - 1053.49794238683*l1**3*l2 - 1053.49794238683*l1**3*l3 + 948.148148148148*l1**3 - 6320.98765432099*l1**2*l2*l3  - \
        1422.22222222222*l1**2*l2 - 1422.22222222222*l1**2*l3 - 8.88888888888889*l1**2 + 2106.99588477366*l1*l2**3 + 3160.49382716049*l1*l2**2*l3  + \
            1422.22222222222*l1*l2**2 + 3160.49382716049*l1*l2*l3**2 - 4.44444444444444*l1*l2 + 2106.99588477366*l1*l3**3 + 1422.22222222222*l1*l3**2 - \
                4.44444444444444*l1*l3 - 4.0*l1 - 1053.49794238683*l2**4 - 1053.49794238683*l2**3*l3 - 474.074074074074*l2**3 + 4.44444444444444*l2**2 -\
                     1053.49794238683*l2*l3**3 + 8.88888888888889*l2*l3 + 2.0*l2 - 1053.49794238683*l3**4 - 474.074074074074*l3**3 + 4.44444444444444*l3**2 + \
                         2.0*l3 - 0.1*sin(3*t)
    f[1]=1053.49794238683*sqrt(3)*l1**3*l2 - 1053.49794238683*sqrt(3)*l1**3*l3 + 474.074074074074*sqrt(3)*l1**2*l2 - 474.074074074074*sqrt(3)*l1**2*l3  -\
         3160.49382716049*sqrt(3)*l1*l2**2*l3 - 474.074074074074*sqrt(3)*l1*l2**2 + 3160.49382716049*sqrt(3)*l1*l2*l3**2 - 4.44444444444444*sqrt(3)*l1*l2 + \
             474.074074074074*sqrt(3)*l1*l3**2 + 4.44444444444444*sqrt(3)*l1*l3 + 1053.49794238683*sqrt(3)*l2**4 - 1053.49794238683*sqrt(3)*l2**3*l3 + \
                 474.074074074074*sqrt(3)*l2**3  - 948.148148148148*sqrt(3)*l2**2*l3 - 4.44444444444444*sqrt(3)*l2**2 + 1053.49794238683*sqrt(3)*l2*l3**3 + \
                     948.148148148148*sqrt(3)*l2*l3**2 - 2.0*sqrt(3)*l2 - 1053.49794238683*sqrt(3)*l3**4 - 474.074074074074*sqrt(3)*l3**3 + \
                         4.44444444444444*sqrt(3)*l3**2 + 2.0*sqrt(3)*l3 - 0.1*cos(3*t)
    f[2]=-158.024691358025*l1**3 - 71.1111111111111*l1**2 + 474.074074074074*l1*l2*l3 + 71.1111111111111*l1*l2 + 71.1111111111111*l1*l3 + l1/3 - \
        158.024691358025*l2**3 - 71.1111111111111*l2**2 + 71.1111111111111*l2*l3 + l2/3 - 158.024691358025*l3**3 - 71.1111111111111*l3**2 + l3/3 + 0.00299999999999997
    
    return f



    
for t in T:

    qd=fsolve(calc_qd,[0, 0, 0],args=(t,)) 
    #print("qd = ", qd)


    #qの算出
    

        #dqdの算出
    dqd=(fsolve(calc_qd,[0, 0, 0],args=(t+0.1,))-fsolve(calc_qd,[0, 0, 0],args=(t,)))/0.1

        #d2qdの算出    
    d2qd= (((fsolve(calc_qd,[0, 0, 0],args=(t+0.2,))-fsolve(calc_qd,[0, 0, 0],args=(t+0.1,)))/0.1)-((fsolve(calc_qd,[0, 0, 0],args=(t+0.1,))-fsolve(calc_qd,[0, 0, 0],args=(t,)))/0.1))/0.1
    
    #print("dqd = ", dqd)
    #print("d2qd = ", d2qd)
    
    

    def fun(q0,t):
        #微分方程式の定義
        dq0dt = np.concatenate(
        [
            q0[0:3],
            -200*q0[0:3]-10000*q0[3:6]+d2qd+200*dqd+10000*qd
           ],
             axis = 0
         )
        print("dq0dt = ", dq0dt)
        return dq0dt


    #微分方程式を解く
sol2 = odeint(
     func = fun,
     y0 = np.zeros(6),
     t=T2
        )     
#print("sol2 = ", sol2)