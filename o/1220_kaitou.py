import numpy as np
from math import sin, cos, sqrt
import matplotlib.pyplot as plt
from scipy.optimize.nonlin import Jacobian
import sympy as sy
import scipy as sp
import scipy.optimize
from scipy.optimize import fsolve
from scipy.integrate import solve_ivp



class Kinematics:
    """ソフトロボットの運動学"""


    def __init__(self,):
        
        self.c1 = 837019575
        self.c2 = 4133430
        self.c3 = 32805
        self.c4 = 486
        self.c5 = 18
        self.c6 = 55801305
        self.c7 = 688905
        self.c8 = 3645
        self.c9 = 81

        self.r = 0.0125
        self.L0 = 0.15


    def calc_X(self, q, xi):
        """アクチュエータ空間からタスク空間への写像
        
        L = [L[0,0], L[1,0], L[2,0]] -> X = [x, y, z]
        """
        
        
        A1 = q[0,0]**2 + q[1,0]**2 + q[1,0]**2 - \
            q[0,0]*q[1,0] - q[0,0]*q[2,0] - q[1,0]*q[2,0]
        A2 = 2*q[0,0] - q[1,0] - q[2,0]
        A3 = q[1,0] - q[2,0]
        A4 = 3*self.L0 + q[0,0] + q[1,0] + q[2,0]
        
        x = -(A2 * A1**4 * A4 * xi**10) / ((self.c1 * self.r**9)) + \
            (A2 * A1**3 * A4 * xi**8) / (self.c2 * self.r**7) - \
                (A2 * A1**2 * A4 * xi**6) / (self.c3 * self.r**5) + \
                    (A2 * A1 * A4 * xi**4) / (self.c4 * self.r**3) - \
                        (A2 * A4 * xi**2) / (self.c5 * self.r)
        
        y = -(sqrt(3) * A4 * A3 * A1**4 * xi**10) / (self.c1 * self.r**9) + \
            (sqrt(3) * A4 * A3 * A1**3 * xi**8) / (self.c2 * self.r**7) - \
                (sqrt(3) * A4 * A3 * A1**2 * xi**6) / (self.c3 * self.r**5) + \
                    (sqrt(3) * A4 * A1 * A2 * xi**4) / (self.c4 * self.r**3) - \
                        (sqrt(3) * A4 * A3 * xi**2) / (self.c5 * self.r)
        
        z = (2 * A1**4 * A4 * xi**9) / (self.c6 * self.r**8) - \
            (4 * A1**3 * A4 * xi**7) / (self.c7 * self.r**6) + \
                (2 * A1**2 * A4 * xi**5) / (self.c8 * self.r**4) - \
                    (2 * A1 *A4 * xi**3) / (self.c9 * self.r**2) + \
                        (A4 * xi) / 3

        return np.array([[x, y, z]]).T


    def calc_Jacobian(self, q, xi):
        """ヤコビ行列
        
        タスク写像XのアクチュエータベクトルLによる偏微分
        """
        
        l1 = q[0,0]
        l2 = q[1,0]
        l3 = q[2,0]
        
        return np.array([
            [
                -xi**2*(2*l1 - l2 - l3)/(self.c5*self.r) - 2*xi**2*(3*self.L0 + l1 + l2 + l3)/(self.c5*self.r) + xi**4*(2*l1 - l2 - l3)**2*(3*self.L0 + l1 + l2 + l3)/(self.c4*self.r**3) + xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) + 2*xi**4*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - xi**6*(2*l1 - l2 - l3)*(4*l1 - 2*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c3*self.r**5) - xi**6*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) - 2*xi**6*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + xi**8*(2*l1 - l2 - l3)*(6*l1 - 3*l2 - 3*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c2*self.r**7) + xi**8*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) + 2*xi**8*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - xi**10*(2*l1 - l2 - l3)*(8*l1 - 4*l2 - 4*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c1*self.r**9) - xi**10*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9) - 2*xi**10*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9),
                -xi**2*(2*l1 - l2 - l3)/(self.c5*self.r) + xi**2*(3*self.L0 + l1 + l2 + l3)/(self.c5*self.r) + xi**4*(-l1 + 4*l2 - l3)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)/(self.c4*self.r**3) + xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - xi**4*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - xi**6*(-2*l1 + 8*l2 - 2*l3)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c3*self.r**5) - xi**6*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + xi**6*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + xi**8*(-3*l1 + 12*l2 - 3*l3)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c2*self.r**7) + xi**8*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - xi**8*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - xi**10*(-4*l1 + 16*l2 - 4*l3)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c1*self.r**9) - xi**10*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9) + xi**10*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9),
                -xi**2*(2*l1 - l2 - l3)/(self.c5*self.r) + xi**2*(3*self.L0 + l1 + l2 + l3)/(self.c5*self.r) + xi**4*(-l1 - l2)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)/(self.c4*self.r**3) + xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - xi**4*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - xi**6*(-2*l1 - 2*l2)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c3*self.r**5) - xi**6*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + xi**6*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + xi**8*(-3*l1 - 3*l2)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c2*self.r**7) + xi**8*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - xi**8*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - xi**10*(-4*l1 - 4*l2)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c1*self.r**9) - xi**10*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9) + xi**10*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9)],
            [
                -sqrt(3)*xi**2*(l2 - l3)/(self.c5*self.r) + sqrt(3)*xi**4*(2*l1 - l2 - l3)**2*(3*self.L0 + l1 + l2 + l3)/(self.c4*self.r**3) + sqrt(3)*xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) + 2*sqrt(3)*xi**4*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - sqrt(3)*xi**6*(l2 - l3)*(4*l1 - 2*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c3*self.r**5) - sqrt(3)*xi**6*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + sqrt(3)*xi**8*(l2 - l3)*(6*l1 - 3*l2 - 3*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c2*self.r**7) + sqrt(3)*xi**8*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - sqrt(3)*xi**10*(l2 - l3)*(8*l1 - 4*l2 - 4*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c1*self.r**9) - sqrt(3)*xi**10*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9),
                -sqrt(3)*xi**2*(l2 - l3)/(self.c5*self.r) - sqrt(3)*xi**2*(3*self.L0 + l1 + l2 + l3)/(self.c5*self.r) + sqrt(3)*xi**4*(-l1 + 4*l2 - l3)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)/(self.c4*self.r**3) + sqrt(3)*xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - sqrt(3)*xi**4*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - sqrt(3)*xi**6*(l2 - l3)*(-2*l1 + 8*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c3*self.r**5) - sqrt(3)*xi**6*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) - sqrt(3)*xi**6*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + sqrt(3)*xi**8*(l2 - l3)*(-3*l1 + 12*l2 - 3*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c2*self.r**7) + sqrt(3)*xi**8*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) + sqrt(3)*xi**8*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - sqrt(3)*xi**10*(l2 - l3)*(-4*l1 + 16*l2 - 4*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c1*self.r**9) - sqrt(3)*xi**10*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9) - sqrt(3)*xi**10*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9),
                -sqrt(3)*xi**2*(l2 - l3)/(self.c5*self.r) + sqrt(3)*xi**2*(3*self.L0 + l1 + l2 + l3)/(self.c5*self.r) + sqrt(3)*xi**4*(-l1 - l2)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)/(self.c4*self.r**3) + sqrt(3)*xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - sqrt(3)*xi**4*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - sqrt(3)*xi**6*(-2*l1 - 2*l2)*(l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c3*self.r**5) - sqrt(3)*xi**6*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + sqrt(3)*xi**6*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + sqrt(3)*xi**8*(-3*l1 - 3*l2)*(l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c2*self.r**7) + sqrt(3)*xi**8*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - sqrt(3)*xi**8*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - sqrt(3)*xi**10*(-4*l1 - 4*l2)*(l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c1*self.r**9) - sqrt(3)*xi**10*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9) + sqrt(3)*xi**10*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9)],
            [
                xi/3 - xi**3*(4*l1 - 2*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)/(self.c9*self.r**2) - xi**3*(2*l1**2 - 2*l1*l2 - 2*l1*l3 + 4*l2**2 - 2*l2*l3)/(self.c9*self.r**2) + 2*xi**5*(4*l1 - 2*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c8*self.r**4) + 2*xi**5*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c8*self.r**4) - 4*xi**7*(6*l1 - 3*l2 - 3*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c7*self.r**6) - 4*xi**7*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c7*self.r**6) + 2*xi**9*(8*l1 - 4*l2 - 4*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c6*self.r**8) + 2*xi**9*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c6*self.r**8),
                xi/3 - xi**3*(-2*l1 + 8*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)/(self.c9*self.r**2) - xi**3*(2*l1**2 - 2*l1*l2 - 2*l1*l3 + 4*l2**2 - 2*l2*l3)/(self.c9*self.r**2) + 2*xi**5*(-2*l1 + 8*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c8*self.r**4) + 2*xi**5*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c8*self.r**4) - 4*xi**7*(-3*l1 + 12*l2 - 3*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c7*self.r**6) - 4*xi**7*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c7*self.r**6) + 2*xi**9*(-4*l1 + 16*l2 - 4*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c6*self.r**8) + 2*xi**9*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c6*self.r**8),
                xi/3 - xi**3*(-2*l1 - 2*l2)*(3*self.L0 + l1 + l2 + l3)/(self.c9*self.r**2) - xi**3*(2*l1**2 - 2*l1*l2 - 2*l1*l3 + 4*l2**2 - 2*l2*l3)/(self.c9*self.r**2) + 2*xi**5*(-2*l1 - 2*l2)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c8*self.r**4) + 2*xi**5*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c8*self.r**4) - 4*xi**7*(-3*l1 - 3*l2)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c7*self.r**6) - 4*xi**7*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c7*self.r**6) + 2*xi**9*(-4*l1 - 4*l2)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c6*self.r**8) + 2*xi**9*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c6*self.r**8)
            ]
        ])




class Dynamics:
    """ソフトロボットの動力学"""
    
    def __init__(self,):
        return 



class PD_FeedbackLinearization_Controller:
    
    Kd = 200
    Kp = 1e4
    
    def __init__(self,):
        pass



class Simulator:
    
    sol = None
    
    def __init__(self, TIME_SPAN, TIME_INTERVAL):
        
        self.TIME_SPAN = TIME_SPAN
        self.TIME_INTERVAL = TIME_INTERVAL
        
        self.Kd = 200
        self.Kp = 1e4
        
        self.kinematics = Kinematics()
    
    
    def xd(self, t):
        return np.array([
            [0.1 * sin(3*t)],
            [0.1 * cos(3*t)],
            [0.147],
        ])


    def xd_dot(self, t):
        return np.array([
            [0.1 * 3 * cos(3*t)],
            [0.1 * 3 * -sin(3*t)],
            [0],
        ])


    def xd_dot_dot(self, t):
        return np.array([
            [0.1 * 9 * -sin(3*t)],
            [0.1 * 9 * -cos(3*t)],
            [0],
        ])


    def calc_q_dot_dot(self, x, x_dot, J, xd, xd_dot, xd_dot_dot):

        z = np.linalg.inv(J) @ \
            (xd_dot_dot - self.Kd*(x_dot - xd_dot) - self.Kp*(x - xd))
        return z


    def state_dot(self, t, state):
        
        q = np.array([state[:3]]).T
        q_dot = np.array([state[3:]]).T
        
        x = self.kinematics.calc_X(q, xi=1)
        J = self.kinematics.calc_Jacobian(q, xi=1)
        x_dot = J @ q_dot
        
        q_dot_dot = self.calc_q_dot_dot(
            x, x_dot, J,
            xd = self.xd(t),
            xd_dot = self.xd_dot(t),
            xd_dot_dot = self.xd_dot_dot(t),
        )
        
        z = np.concatenate([q_dot, q_dot_dot])
        
        return np.ravel(z)



    def run_simulation(self,):
        """動力学なしで軌道追従をシミュレーション"""
        
        
        q_init = np.array([[0, 0, 0]]).T
        dq_init = np.zeros((3, 1))
        ddq_init = np.zeros((3, 1))
        
        state_init = np.concatenate([q_init, dq_init])
        
        self.sol = solve_ivp(
            fun = self.state_dot,
            t_span = (0, self.TIME_SPAN),
            y0 = np.ravel(state_init)
        )
        
        return
    
    
    def plot_actuator_data(self,):
        
        if self.sol is None:
            return
        
        else:
            fig = plt.figure()
            ax = fig.add_subplot(1, 2, 1)
            ax.plot(self.sol.t, self.sol.y[0], label = "l1")
            ax.plot(self.sol.t, self.sol.y[1], label = "l2")
            ax.plot(self.sol.t, self.sol.y[2], label = "l3")
            ax.legend()
            
            ax2 = fig.add_subplot(1, 2, 2)
            ax2.plot(self.sol.t, self.sol.y[3], label = "l1_dot")
            ax2.plot(self.sol.t, self.sol.y[4], label = "l2_dot")
            ax2.plot(self.sol.t, self.sol.y[5], label = "l3_dot")
            ax2.legend()
            
            plt.show()
    
    
    def make_animation(self,):
        
        






if __name__ == "__main__":
    
    hoge = Simulator(3, 0.01)
    
    hoge.run_simulation()
    hoge.plot_actuator_data()
    




# def func(L):
#     X = calc_X(L.reshape(3,1), xi=1)
#     return np.ravel(X)

# xd = [0, 0, 0.3]

# sol = fsolve(func, xd)


# L = np.array([[sol[0],sol[1],sol[2]]]).T
# L = np.array([[-0.25,-0.25,0.05]]).T
# print(L)
# xi_all = np.arange(0, 1, 0.01)

# Xs = np.concatenate([calc_X(L, xi).T for xi in xi_all])
# print(Xs)

# fig = plt.figure()
# ax = fig.add_subplot(projection = '3d')
# ax.plot(Xs[:, 0], Xs[:, 1], Xs[:, 2], label="arm")

# #ax.scatter([xd[0]], [xd[1]], [xd[2]], label="xd")

# ax.legend()



# # x_max = 0.2
# # x_min = -0.2
# # y_max = 0.2
# # y_min = -0.2
# # z_max = 0.2
# # z_min = 0
# # max_range = max(x_max-x_min, y_max-y_min, z_max-z_min)*0.5
# # x_mid = (x_max + x_min) / 2
# # y_mid = (y_max + y_min) / 2
# # z_mid = (z_max + z_min) / 2

# # ax.set_xlim(x_mid-max_range, x_mid+max_range)
# # ax.set_ylim(y_mid-max_range, y_mid+max_range)
# # ax.set_zlim(z_mid-max_range, z_mid+max_range)

# ax.set_box_aspect((1,1,1))

# plt.show()