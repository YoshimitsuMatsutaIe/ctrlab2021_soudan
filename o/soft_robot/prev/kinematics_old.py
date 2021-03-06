import numpy as np
from math import sin, cos, sqrt

import linearized_J_dot



class KinematicsOfOneSection:
    """1つのセクションの運動学"""
    
    def __init__(self,):
        
        self.xi_all = np.arange(0, 1, 0.05)  # xi一覧
        
        # 線形化した後のパラメータ
        self.c1 = 837019575
        self.c2 = 4133430
        self.c3 = 32805
        self.c4 = 486
        self.c5 = 18
        self.c6 = 55801305
        self.c7 = 688905
        self.c8 = 3645
        self.c9 = 81
        
        self.c10 = 279006525
        self.c11 = 1377810
        self.c12 = 10935
        self.c13 = 162

        self.c14 = 243
        self.c15 = 2066715

        self.r = 0.0125
        self.L0 = 0.15
        
        self.sq3 = sqrt(3)


    def mapping_from_actuator_to_configuration(self, q, xi):
        """アクチュエータ空間から配置空間への写像"""
        
        l1 = q[0,0]
        l2 = q[1,0]
        l3 = q[2,0]
        
        A1 = l1**2 + l2**2 + l3**2 - \
            l1*l2 - l1*l3 - l2*l3
        A2 = 2*l1 - l2 - l3
        A3 = l2 - l3
        A4 = 3*self.L0 + l1 + l2 + l3
        
        #print("A1 =", A1)
        if A1 < 1e-6:
            lam = A4 * self.r / 2*1e-6
        else:
            lam = A4 * self.r / 2*sqrt(A1)
        phi = 2*sqrt(A1) / 3*self.r
        theta = np.arctan2(self.sq3 * (-A3) / (-A2), 1)
        
        if phi <= 0 or phi > 2*np.pi:
            print("phiが範囲外!")
        
        if theta <= -np.pi or theta >= np.pi:
            print("thetaが範囲外")
        
        return np.array([[lam, phi, theta]]).T


    def mapping_from_configration_to_task_p(self, c, xi):
        """配置空間からタスク空間pへの写像"""
        
        lam = c[0, 0]
        phi = c[1, 0]
        theta = c[2, 0]
        
        return np.array([
            [lam * cos(theta) * (1 - cos(xi * phi))],
            [lam * sin(theta) * (1 - cos(xi * phi))],
            [lam * sin(xi * phi)],
        ])


    def mapping_from_configration_to_task_R(self, c, xi):
        """配置空間からタスク空間Rへの写像"""
        
        lam = c[0, 0]
        phi = c[1, 0]
        theta = c[2, 0]
        
        R11 = cos(theta)**2 * cos(xi*phi) + sin(theta)**2
        R12 = sin(theta) * cos(theta) * (cos(xi*phi) - 1)
        R13 = cos(theta) * sin(xi*phi)
        R21 = R12
        R22 = sin(theta)**2 * cos(xi*phi) + cos(theta)**2
        R23 = sin(theta) * sin(xi*phi)
        R31 = -R13
        R32 = -R23
        R33 = cos(xi*phi)
        
        return np.array([
            [R11, R12, R13],
            [R21, R22, R23],
            [R31, R32, R33],
        ])


    def mapping_from_actuator_to_task_p(self, q, xi=1):
        """アクチュエータ空間からタスク空間への写像"""
        
        c = self.mapping_from_actuator_to_configuration(q, xi)
        #print("c = ", c)
        x = self.mapping_from_configration_to_task_p(c, xi)
        #print("x = ", x)
        return x

    def calc_all_task_ps(self, q):
        # return np.concatenate(
        #     [self.mapping_from_actuator_to_task_p(q, xi).T for xi in self.xi_all]
        # )
        return np.concatenate(
            [self.linearized_mapping_from_actuator_to_task_p(q, xi).T for xi in self.xi_all]
        )

    def mapping_from_actuator_to_task_R(self, q, xi):
        """アクチュエータ空間からタスク空間への写像"""
        
        c = self.mapping_from_actuator_to_configuration(q, xi)
        R = self.mapping_from_configration_to_task_R(c, xi)
        
        return R


    def HTM(self, q, xi):
        """同時変換行列"""
        
        c = self.mapping_from_actuator_to_configuration(q, xi)
        p = self.mapping_from_configration_to_task_p(c, xi)
        R = self.mapping_from_configration_to_task_R(c, xi)

        return np.block([
            [R, p],
            [np.zeros((1, 3)), np.eye(1)],
        ])


    def jacobian_dcdq(self, q, xi):
        """配置空間のアクチュエータ空間による偏微分"""
        
        l1 = q[0,0]
        l2 = q[1,0]
        l3 = q[2,0]
        A1 = l1**2 + l2**2 + l3**2 - l1*l2 - l1*l3 - l2*l3
        A2 = 2*l1 - l2 - l3
        A4 = 3*self.L0 + l1 + l2 + l3
        
        return np.array([
            [
                (l1 - l2/2 - l3/2)*(3*self.L0/2 + l1/2 + l2/2 + l3/2)/sqrt(A1) + sqrt(A1)/2,
                (-l1/2 + l2 - l3/2)*(3*self.L0/2 + l1/2 + l2/2 + l3/2)/sqrt(A1) + sqrt(A1)/2,
                (-l1/2 - l2/2 + l3)*(3*self.L0/2 + l1/2 + l2/2 + l3/2)/sqrt(A1) + sqrt(A1)/2
            ],
            [
                2*self.r*(l1 - l2/2 - l3/2)/(3*sqrt(A1)),
                2*self.r*(-l1/2 + l2 - l3/2)/(3*sqrt(A1)),
                2*self.r*(-l1/2 - l2/2 + l3)/(3*sqrt(A1))
            ],
            [
                2*self.sq3*(-l2 + l3)/((3*(-l2 + l3)**2/(-A2)**2 + 1)*(-A2)**2),
                (-self.sq3*(-l2 + l3)/(-A2)**2 - self.sq3/(-A2))/(3*(-l2 + l3)**2/(-A2)**2 + 1),
                (-self.sq3*(-l2 + l3)/(-A2)**2 + self.sq3/(-A2))/(3*(-l2 + l3)**2/(-A2)**2 + 1)
            ]
        ])

    def jacobian_dpdc(self, c, xi):
        """タスク空間の配置空間による偏微分"""
        
        lam = c[0, 0]
        phi = c[1, 0]
        theta = c[2, 0]
        
        return np.array([
            [(1 - cos(phi*xi))*cos(theta), lam*xi*sin(phi*xi)*cos(theta), -lam*(1 - cos(phi*xi))*sin(theta)],
            [(1 - cos(phi*xi))*sin(theta), lam*xi*sin(theta)*sin(phi*xi), lam*(1 - cos(phi*xi))*cos(theta)],
            [sin(phi*xi), lam*xi*cos(phi*xi), 0]
        ])


    def jacobian_dpdq(self, q, xi):
        """タスク空間のアクチュエータ空間による偏微分"""
        
        # c = self.mapping_from_actuator_to_configuration(q, xi)
        
        # dcdq = self.jacobian_dcdq(q, xi)
        # dpdc = self.jacobian_dpdc(c, xi)
        
        # J =  dpdc @ dcdq
        
        l1 = q[0,0]
        l2 = q[1,0]
        l3 = q[2,0]
        A1 = l1**2 + l2**2 + l3**2 - l1*l2 - l1*l3 - l2*l3
        A2 = 2*l1 - l2 - l3
        A4 = 3*self.L0 + l1 + l2 + l3
        
        J = np.array([
            [
                (3*(l2 - l3)**2 + (-A2)**2)*(36*(l2 - l3)**2*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(3*self.L0 + l1 + l2 + l3)*(A1) + 2*(-self.r*xi*(-A2)*(A4)*sin(2*self.r*xi*sqrt(A1)/3) + 6*sqrt(A1)*sin(self.r*xi*sqrt(A1)/3)**2)*(3*(l2 - l3)**2 + (-A2)**2)*(-A2)*sqrt(A1) + 3*(3*(l2 - l3)**2 + (-A2)**2)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(-A2)**2*(A4))/(12*((3*(l2 - l3)**2 + (-A2)**2)/(-A2)**2)**(5/2)*(-A2)**5*sqrt(A1)),
                (3*(l2 - l3)**2 + (-A2)**2)*(-18*((-l2 + l3)*(-A2) + (l2 - l3)**2)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(A4)*(A1) + 2*(-self.r*xi*(l1 - 2*l2 + l3)*(A4)*sin(2*self.r*xi*sqrt(A1)/3) + 6*sqrt(A1)*sin(self.r*xi*sqrt(A1)/3)**2)*(3*(l2 - l3)**2 + (-A2)**2)*(-A2)*sqrt(A1) + 3*(3*(l2 - l3)**2 + (-A2)**2)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(-A2)*(l1 - 2*l2 + l3)*(A4))/(12*((3*(l2 - l3)**2 + (-A2)**2)/(-A2)**2)**(5/2)*(-A2)**5*sqrt(A1)),
                (3*(l2 - l3)**2 + (-A2)**2)*(-36*(-l1 + l2)*(l2 - l3)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(A4)*(A1) + 2*(-self.r*xi*(l1 + l2 - 2*l3)*(A4)*sin(2*self.r*xi*sqrt(A1)/3) + 6*sqrt(A1)*sin(self.r*xi*sqrt(A1)/3)**2)*(3*(l2 - l3)**2 + (-A2)**2)*(-A2)*sqrt(A1) + 3*(3*(l2 - l3)**2 + (-A2)**2)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(-A2)*(l1 + l2 - 2*l3)*(A4))/(12*((3*(l2 - l3)**2 + (-A2)**2)/(-A2)**2)**(5/2)*(-A2)**5*sqrt(A1))
            ],
            [
                self.sq3*(l2 - l3)*(3*(l2 - l3)**2 + (-A2)**2)**2*(2*self.r*xi*(3*(l2 - l3)**2 + (-A2)**2)*(-A2)**2*(A4)*sqrt(A1)*sin(2*self.r*xi*sqrt(A1)/3) - 36*(l2 - l3)**2*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(A4)*(A1) - 3*(3*(l2 - l3)**2 + (-A2)**2)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(-A2)**2*(A4) + 6*(3*(l2 - l3)**2 + (-A2)**2)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(-A2)*(A1) + 12*(3*(l2 - l3)**2 + (-A2)**2)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(A4)*(A1))/(12*((3*(l2 - l3)**2 + (-A2)**2)/(-A2)**2)**(7/2)*(-A2)**8*sqrt(A1)),
                self.sq3*((3*(l2 - l3)**2 + (-A2)**2)/(-A2)**2)**(3/2)*(-A2)**2*(18*(l2 - l3)*((-l2 + l3)*(-A2) + (l2 - l3)**2)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(A4)*(A1) - 3*(l2 - l3)*(3*(l2 - l3)**2 + (-A2)**2)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(-A2)*(l1 - 2*l2 + l3)*(A4) - 6*(l2 - l3)*(3*(l2 - l3)**2 + (-A2)**2)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(A4)*(A1) + 2*(3*(l2 - l3)**2 + (-A2)**2)*(-A2)*(self.r*xi*(l2 - l3)*(l1 - 2*l2 + l3)*(A4)*sin(2*self.r*xi*sqrt(A1)/3) + 3*(l2 - l3)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*sqrt(A1) + 3*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(A4)*sqrt(A1))*sqrt(A1))/(12*(3*(l2 - l3)**2 + (-A2)**2)**3*sqrt(A1)),
                self.sq3*((3*(l2 - l3)**2 + (-A2)**2)/(-A2)**2)**(3/2)*(-A2)**2*(3*(-l1 + l2)*(l2 - l3)**2*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(A4)*(A1) - (l2 - l3)*(3*(l2 - l3)**2 + (-A2)**2)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(-A2)*(l1 + l2 - 2*l3)*(A4)/4 - (l2 - l3)*(3*(l2 - l3)**2 + (-A2)**2)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(A4)*(A1)/2 + (3*(l2 - l3)**2 + (-A2)**2)*(-A2)*(self.r*xi*(l2 - l3)*(l1 + l2 - 2*l3)*(A4)*sin(2*self.r*xi*sqrt(A1)/3) + 3*(l2 - l3)*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*sqrt(A1) - 3*(cos(2*self.r*xi*sqrt(A1)/3) - 1)*(A4)*sqrt(A1))*sqrt(A1)/6)/((3*(l2 - l3)**2 + (-A2)**2)**3*sqrt(A1))
            ],
            [
                (2*(-self.r*xi*(-A2)*(A4)*cos(2*self.r*xi*sqrt(A1)/3) + 3*sqrt(A1)*sin(2*self.r*xi*sqrt(A1)/3))*sqrt(A1) - 3*(-A2)*(A4)*sin(2*self.r*xi*sqrt(A1)/3))/(12*sqrt(A1)),
                (2*(-self.r*xi*(l1 - 2*l2 + l3)*(A4)*cos(2*self.r*xi*sqrt(A1)/3) + 3*sqrt(A1)*sin(2*self.r*xi*sqrt(A1)/3))*sqrt(A1) - 3*(l1 - 2*l2 + l3)*(A4)*sin(2*self.r*xi*sqrt(A1)/3))/(12*sqrt(A1)),
                (2*(-self.r*xi*(l1 + l2 - 2*l3)*(A4)*cos(2*self.r*xi*sqrt(A1)/3) + 3*sqrt(A1)*sin(2*self.r*xi*sqrt(A1)/3))*sqrt(A1) - 3*(l1 + l2 - 2*l3)*(A4)*sin(2*self.r*xi*sqrt(A1)/3))/(12*sqrt(A1))
            ]
        ])
        
        return J


    def linearized_mapping_from_actuator_to_task_p(self, q, xi=1):
        """線形化されたアクチュエータ空間からタスク空間への写像
        
        順運動学
        """
        
        l1 = q[0,0]
        l2 = q[1,0]
        l3 = q[2,0]
        
        A1 = l1**2 + l2**2 + l3**2 - l1*l2 - l1*l3 - l2*l3
        A2 = 2*l1 - l2 - l3
        A3 = l2 - l3
        A4 = 3*self.L0 + l1 + l2 + l3
        
        x = -(A2 * A1**4 * A4 * xi**10) / ((self.c1 * self.r**9)) + \
            (A2 * A1**3 * A4 * xi**8) / (self.c2 * self.r**7) - \
                (A2 * A1**2 * A4 * xi**6) / (self.c3 * self.r**5) + \
                    (A2 * A1 * A4 * xi**4) / (self.c4 * self.r**3) - \
                        (A2 * A4 * xi**2) / (self.c5 * self.r)
        
        y = -(self.sq3 * A4 * A3 * A1**4 * xi**10) / (self.c1 * self.r**9) + \
            (self.sq3 * A4 * A3 * A1**3 * xi**8) / (self.c2 * self.r**7) - \
                (self.sq3 * A4 * A3 * A1**2 * xi**6) / (self.c3 * self.r**5) + \
                    (self.sq3 * A4 * A1 * A2 * xi**4) / (self.c4 * self.r**3) - \
                        (self.sq3 * A4 * A3 * xi**2) / (self.c5 * self.r)
        
        z = (2 * A1**4 * A4 * xi**9) / (self.c6 * self.r**8) - \
            (4 * A1**3 * A4 * xi**7) / (self.c7 * self.r**6) + \
                (2 * A1**2 * A4 * xi**5) / (self.c8 * self.r**4) - \
                    (2 * A1 *A4 * xi**3) / (self.c9 * self.r**2) + \
                        (A4 * xi) / 3

        return np.array([[x, y, z]]).T


    def linearized_mapping_from_actuator_to_task_R(self, q, xi):
        """線形化された回転行列"""
        
        l1 = q[0,0]
        l2 = q[1,0]
        l3 = q[2,0]
        
        A1 = l1**2 + l2**2 + l3**2 - l1*l2 - l1*l3 - l2*l3
        A2 = 2*l1 - l2 - l3
        A3 = l2 - l3
        A4 = 3*self.L0 + l1 + l2 + l3
        
        R11 = 1 - (A2**2 * A1**4 * xi**10) / (self.c1 * self.r**10) + \
            (A2**2 * A1**3 * xi**8) / (self.c1 * self.r**8) - \
                (A2**2 * A1**2 * xi**6) / (self.c3 * self.r**6) + \
                    (A1 * A2**2 * xi**4) / (self.c4 * self.r**4) - \
                        (A2**2 * xi**2) / (self.c5 * self.r**2)
        
        R12 = (self.sq3 * A2 * A3 * A1**4 * xi**10) / (self.c1 * self.r**10) + \
            (self.sq3 * A2 * A3 * A1**3 * xi**8) / (self.c2 * self.r**8) - \
                (self.sq3 * A2 * A3 * A1**2 * xi**6) / (self.c3 * self.r**6) + \
                    (self.sq3 * A2 * A3 * A1 * xi**4) / (self.c4 * self.r**4) - \
                        (self.sq3 * A2 * A3 * xi**2) / (self.c5 * self.r**2)
        
        R13 = -(2 * A2 * A1**4 * xi**9) / (self.c6 * self.r**9) + \
            (4 * A2 * A1**3 * xi**7) / (self.c7 * self.r**7) - \
                (2 * A2 * A1**2 * xi**5) / (self.c8 * self.r**5) + \
                    (2 * A2 * A1 * xi**3) / (self.c9 * self.r**3) - \
                        (A2 * xi) / (3 * self.r)
        
        R22 = 1 - (A3**2 * A1**4 * xi**10) / (self.c10 * self.r**10) + \
            (A3**2 * A1**3 * xi**8) / (self.c11 * self.r**8) - \
                (A3**2 * A1**2 * xi**6) / (self.c12 * self.r**6) + \
                    (A3**2 * A1 * xi**4) / (self.c13 * self.r**4) - \
                        (A3**2 * xi**2) / (6 * self.r**2)
        
        R23 = -(2*self.sq3 * A3 * A1**4 * xi**9) / (self.c6 * self.r**9) + \
            (4*self.sq3 * A3 * A1**3 * xi**7) / (self.c7 * self.r**7) - \
                (2*self.sq3 * A3 * A1**2 * xi**5) / (self.c8 * self.r**5) + \
                    (2*self.sq3 * A3 * A1 * xi**3) / (self.c9 * self.r**3) - \
                        (self.sq3 * A3 * xi) / (3 * self.r)
        
        R33 = 1 - (2 * xi**2 * A1) / (9 * self.r**2) + \
            (2 * xi**4 * A1**2) / (self.c14 * self.r**4) - \
                (4 * xi**6 * A1**3) / (self.c3 * self.r**6) + \
                    (2 * xi**8 * A1**4) / (self.c15 * self.r**8) - \
                        (4 * xi**10 * A1**5) / (self.c1 * self.r**10)
        
        R21 = R12
        R31 = -R13
        R32 = -R23
        
        return np.array([
            [R11, R12, R13],
            [R21, R22, R23],
            [R31, R32, R33],
        ])


    def MHTM(self, q, xi):
        """モーダル同時変換行列
        
        線形化されたHomogeneous Transformation Matrix
        """
        
        p = self.linearized_mapping_from_actuator_to_task_p(q, xi)
        R = self.linearized_mapping_from_actuator_to_task_R(q, xi)
        
        return np.block([
            [R, p],
            [np.zeros((1, 3)), np.eye(1)],
        ])


    def linearized_dpdl1(self, q, xi):
        l1 = q[0,0]
        l2 = q[1,0]
        l3 = q[2,0]
        
        return np.array([[
            -xi**2*(2*l1 - l2 - l3)/(self.c5*self.r) - 2*xi**2*(3*self.L0 + l1 + l2 + l3)/(self.c5*self.r) + xi**4*(2*l1 - l2 - l3)**2*(3*self.L0 + l1 + l2 + l3)/(self.c4*self.r**3) + xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) + 2*xi**4*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - xi**6*(2*l1 - l2 - l3)*(4*l1 - 2*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c3*self.r**5) - xi**6*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) - 2*xi**6*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + xi**8*(2*l1 - l2 - l3)*(6*l1 - 3*l2 - 3*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c2*self.r**7) + xi**8*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) + 2*xi**8*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - xi**10*(2*l1 - l2 - l3)*(8*l1 - 4*l2 - 4*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c1*self.r**9) - xi**10*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9) - 2*xi**10*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9),
            -self.sq3*xi**2*(l2 - l3)/(self.c5*self.r) + self.sq3*xi**4*(2*l1 - l2 - l3)**2*(3*self.L0 + l1 + l2 + l3)/(self.c4*self.r**3) + self.sq3*xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) + 2*self.sq3*xi**4*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - self.sq3*xi**6*(l2 - l3)*(4*l1 - 2*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c3*self.r**5) - self.sq3*xi**6*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + self.sq3*xi**8*(l2 - l3)*(6*l1 - 3*l2 - 3*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c2*self.r**7) + self.sq3*xi**8*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - self.sq3*xi**10*(l2 - l3)*(8*l1 - 4*l2 - 4*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c1*self.r**9) - self.sq3*xi**10*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9),
            xi/3 - xi**3*(4*l1 - 2*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)/(self.c9*self.r**2) - xi**3*(2*l1**2 - 2*l1*l2 - 2*l1*l3 + 4*l2**2 - 2*l2*l3)/(self.c9*self.r**2) + 2*xi**5*(4*l1 - 2*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c8*self.r**4) + 2*xi**5*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c8*self.r**4) - 4*xi**7*(6*l1 - 3*l2 - 3*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c7*self.r**6) - 4*xi**7*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c7*self.r**6) + 2*xi**9*(8*l1 - 4*l2 - 4*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c6*self.r**8) + 2*xi**9*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c6*self.r**8),
        ]]).T

    def linearized_dpdl2(self, q, xi):
        l1 = q[0,0]
        l2 = q[1,0]
        l3 = q[2,0]
        
        return np.array([[
            -xi**2*(2*l1 - l2 - l3)/(self.c5*self.r) + xi**2*(3*self.L0 + l1 + l2 + l3)/(self.c5*self.r) + xi**4*(-l1 + 4*l2 - l3)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)/(self.c4*self.r**3) + xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - xi**4*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - xi**6*(-2*l1 + 8*l2 - 2*l3)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c3*self.r**5) - xi**6*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + xi**6*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + xi**8*(-3*l1 + 12*l2 - 3*l3)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c2*self.r**7) + xi**8*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - xi**8*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - xi**10*(-4*l1 + 16*l2 - 4*l3)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c1*self.r**9) - xi**10*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9) + xi**10*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9),
            -self.sq3*xi**2*(l2 - l3)/(self.c5*self.r) - self.sq3*xi**2*(3*self.L0 + l1 + l2 + l3)/(self.c5*self.r) + self.sq3*xi**4*(-l1 + 4*l2 - l3)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)/(self.c4*self.r**3) + self.sq3*xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - self.sq3*xi**4*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - self.sq3*xi**6*(l2 - l3)*(-2*l1 + 8*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c3*self.r**5) - self.sq3*xi**6*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) - self.sq3*xi**6*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + self.sq3*xi**8*(l2 - l3)*(-3*l1 + 12*l2 - 3*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c2*self.r**7) + self.sq3*xi**8*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) + self.sq3*xi**8*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - self.sq3*xi**10*(l2 - l3)*(-4*l1 + 16*l2 - 4*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c1*self.r**9) - self.sq3*xi**10*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9) - self.sq3*xi**10*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9),
            xi/3 - xi**3*(-2*l1 + 8*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)/(self.c9*self.r**2) - xi**3*(2*l1**2 - 2*l1*l2 - 2*l1*l3 + 4*l2**2 - 2*l2*l3)/(self.c9*self.r**2) + 2*xi**5*(-2*l1 + 8*l2 - 2*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c8*self.r**4) + 2*xi**5*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c8*self.r**4) - 4*xi**7*(-3*l1 + 12*l2 - 3*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c7*self.r**6) - 4*xi**7*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c7*self.r**6) + 2*xi**9*(-4*l1 + 16*l2 - 4*l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c6*self.r**8) + 2*xi**9*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c6*self.r**8),
        ]]).T

    def linearized_dpdl3(self, q, xi):
        l1 = q[0,0]
        l2 = q[1,0]
        l3 = q[2,0]

        return np.array([[
            -xi**2*(2*l1 - l2 - l3)/(self.c5*self.r) + xi**2*(3*self.L0 + l1 + l2 + l3)/(self.c5*self.r) + xi**4*(-l1 - l2)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)/(self.c4*self.r**3) + xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - xi**4*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - xi**6*(-2*l1 - 2*l2)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c3*self.r**5) - xi**6*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + xi**6*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + xi**8*(-3*l1 - 3*l2)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c2*self.r**7) + xi**8*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - xi**8*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - xi**10*(-4*l1 - 4*l2)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c1*self.r**9) - xi**10*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9) + xi**10*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9),
            -self.sq3*xi**2*(l2 - l3)/(self.c5*self.r) + self.sq3*xi**2*(3*self.L0 + l1 + l2 + l3)/(self.c5*self.r) + self.sq3*xi**4*(-l1 - l2)*(2*l1 - l2 - l3)*(3*self.L0 + l1 + l2 + l3)/(self.c4*self.r**3) + self.sq3*xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - self.sq3*xi**4*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c4*self.r**3) - self.sq3*xi**6*(-2*l1 - 2*l2)*(l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c3*self.r**5) - self.sq3*xi**6*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + self.sq3*xi**6*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c3*self.r**5) + self.sq3*xi**8*(-3*l1 - 3*l2)*(l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c2*self.r**7) + self.sq3*xi**8*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - self.sq3*xi**8*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c2*self.r**7) - self.sq3*xi**10*(-4*l1 - 4*l2)*(l2 - l3)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c1*self.r**9) - self.sq3*xi**10*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9) + self.sq3*xi**10*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c1*self.r**9),
            xi/3 - xi**3*(-2*l1 - 2*l2)*(3*self.L0 + l1 + l2 + l3)/(self.c9*self.r**2) - xi**3*(2*l1**2 - 2*l1*l2 - 2*l1*l3 + 4*l2**2 - 2*l2*l3)/(self.c9*self.r**2) + 2*xi**5*(-2*l1 - 2*l2)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)/(self.c8*self.r**4) + 2*xi**5*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c8*self.r**4) - 4*xi**7*(-3*l1 - 3*l2)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**2/(self.c7*self.r**6) - 4*xi**7*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c7*self.r**6) + 2*xi**9*(-4*l1 - 4*l2)*(3*self.L0 + l1 + l2 + l3)*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**3/(self.c6*self.r**8) + 2*xi**9*(l1**2 - l1*l2 - l1*l3 + 2*l2**2 - l2*l3)**4/(self.c6*self.r**8)
        ]]).T


    def linearized_jacobian_dpdq(self, q, xi):
        """ヤコビ行列
        
        タスク写像XのアクチュエータベクトルLによる偏微分
        """
        
        return np.block([[
            self.linearized_dpdl1(q, xi),
            self.linearized_dpdl2(q, xi),
            self.linearized_dpdl3(q, xi),
        ]])


    def linearized_jacobian_dpdq_dot(self, q, q_dot, xi):
        """ヤコビ行列の時間微分
        
        タスク写像XのアクチュエータベクトルLによる偏微分の時間微分
        """
        
        return linearized_J_dot.f(
            q[0,0], q[1,0], q[2,0],
            q_dot[0,0], q_dot[1,0], q_dot[2,0],
            xi, self.r, self.L0,
            self.c1, self.c2, self.c3, self.c4, self.c5,
            self.c6, self.c7, self.c8, self.c9
        )
    
    
    def linearized_dRdl1(self, q, xi):
        l1 = q[0,0]
        l2 = q[1,0]
        l3 = q[2,0]
        return np.array([
            [
                -xi**2*(8*l1 - 4*l2 - 4*l3)/(self.c5*self.r**2) + xi**4*(2*l1 - l2 - l3)**3/(self.c4*self.r**4) + xi**4*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c4*self.r**4) - xi**6*(2*l1 - l2 - l3)**2*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c3*self.r**6) - xi**6*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) + xi**8*(2*l1 - l2 - l3)**2*(6*l1 - 3*l2 - 3*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c1*self.r**8) + xi**8*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c1*self.r**8) - xi**10*(2*l1 - l2 - l3)**2*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c1*self.r**10) - xi**10*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10), 
                -2*self.sq3*xi**2*(l2 - l3)/(self.c5*self.r**2) + self.sq3*xi**4*(l2 - l3)*(2*l1 - l2 - l3)**2/(self.c4*self.r**4) + 2*self.sq3*xi**4*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c4*self.r**4) - self.sq3*xi**6*(l2 - l3)*(2*l1 - l2 - l3)*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c3*self.r**6) - 2*self.sq3*xi**6*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) + self.sq3*xi**8*(l2 - l3)*(2*l1 - l2 - l3)*(6*l1 - 3*l2 - 3*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c2*self.r**8) + 2*self.sq3*xi**8*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c2*self.r**8) + self.sq3*xi**10*(l2 - l3)*(2*l1 - l2 - l3)*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c1*self.r**10) + 2*self.sq3*xi**10*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10),
                -2*xi/(3*self.r) + xi**3*(2*l1 - l2 - l3)*(4*l1 - 2*l2 - 2*l3)/(self.c9*self.r**3) + 4*xi**3*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c9*self.r**3) - xi**5*(4*l1 - 2*l2 - 2*l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c8*self.r**5) - 4*xi**5*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c8*self.r**5) + xi**7*(6*l1 - 3*l2 - 3*l3)*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c7*self.r**7) + 8*xi**7*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c7*self.r**7) - xi**9*(4*l1 - 2*l2 - 2*l3)*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c6*self.r**9) - 4*xi**9*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c6*self.r**9)
            ], 
            [
                -2*self.sq3*xi**2*(l2 - l3)/(self.c5*self.r**2) + self.sq3*xi**4*(l2 - l3)*(2*l1 - l2 - l3)**2/(self.c4*self.r**4) + 2*self.sq3*xi**4*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c4*self.r**4) - self.sq3*xi**6*(l2 - l3)*(2*l1 - l2 - l3)*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c3*self.r**6) - 2*self.sq3*xi**6*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) + self.sq3*xi**8*(l2 - l3)*(2*l1 - l2 - l3)*(6*l1 - 3*l2 - 3*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c2*self.r**8) + 2*self.sq3*xi**8*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c2*self.r**8) + self.sq3*xi**10*(l2 - l3)*(2*l1 - l2 - l3)*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c1*self.r**10) + 2*self.sq3*xi**10*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10), 
                xi**4*(l2 - l3)**2*(2*l1 - l2 - l3)/(self.c13*self.r**4) - xi**6*(l2 - l3)**2*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c12*self.r**6) + xi**8*(l2 - l3)**2*(6*l1 - 3*l2 - 3*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c11*self.r**8) - xi**10*(l2 - l3)**2*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c10*self.r**10),
                2*self.sq3*xi**3*(l2 - l3)*(2*l1 - l2 - l3)/(self.c9*self.r**3) - 2*self.sq3*xi**5*(l2 - l3)*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c8*self.r**5) + 4*self.sq3*xi**7*(l2 - l3)*(6*l1 - 3*l2 - 3*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c7*self.r**7) - 2*self.sq3*xi**9*(l2 - l3)*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c6*self.r**9)
            ],
            [
                2*xi/(3*self.r) - xi**3*(2*l1 - l2 - l3)*(4*l1 - 2*l2 - 2*l3)/(self.c9*self.r**3) - 4*xi**3*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c9*self.r**3) + xi**5*(4*l1 - 2*l2 - 2*l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c8*self.r**5) + 4*xi**5*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c8*self.r**5) - xi**7*(6*l1 - 3*l2 - 3*l3)*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c7*self.r**7) - 8*xi**7*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c7*self.r**7) + xi**9*(4*l1 - 2*l2 - 2*l3)*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c6*self.r**9) + 4*xi**9*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c6*self.r**9),
                -2*self.sq3*xi**3*(l2 - l3)*(2*l1 - l2 - l3)/(self.c9*self.r**3) + 2*self.sq3*xi**5*(l2 - l3)*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c8*self.r**5) - 4*self.sq3*xi**7*(l2 - l3)*(6*l1 - 3*l2 - 3*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c7*self.r**7) + 2*self.sq3*xi**9*(l2 - l3)*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c6*self.r**9),
                -2*xi**2*(2*l1 - l2 - l3)/(9*self.r**2) - 4*xi**6*(6*l1 - 3*l2 - 3*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) + 2*xi**8*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c15*self.r**8) + 2*xi**4*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c14*self.r**4) - 4*xi**10*(10*l1 - 5*l2 - 5*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10)
            ]
        ])
    
    
    def linearized_dRdl2(self, q, xi):
        l1 = q[0,0]
        l2 = q[1,0]
        l3 = q[2,0]
        return np.array([
            [
                -xi**2*(-4*l1 + 2*l2 + 2*l3)/(self.c5*self.r**2) + xi**4*(-4*l1 + 2*l2 + 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c4*self.r**4) + xi**4*(-l1 + 2*l2 - l3)*(2*l1 - l2 - l3)**2/(self.c4*self.r**4) - xi**6*(-4*l1 + 2*l2 + 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) - xi**6*(-2*l1 + 4*l2 - 2*l3)*(2*l1 - l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c3*self.r**6) + xi**8*(-4*l1 + 2*l2 + 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c1*self.r**8) + xi**8*(-3*l1 + 6*l2 - 3*l3)*(2*l1 - l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c1*self.r**8) - xi**10*(-4*l1 + 2*l2 + 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10) - xi**10*(-4*l1 + 8*l2 - 4*l3)*(2*l1 - l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c1*self.r**10), 
                self.sq3*xi**2*(l2 - l3)/(self.c5*self.r**2) - self.sq3*xi**2*(2*l1 - l2 - l3)/(self.c5*self.r**2) + self.sq3*xi**4*(l2 - l3)*(-l1 + 2*l2 - l3)*(2*l1 - l2 - l3)/(self.c4*self.r**4) - self.sq3*xi**4*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c4*self.r**4) + self.sq3*xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c4*self.r**4) - self.sq3*xi**6*(l2 - l3)*(-2*l1 + 4*l2 - 2*l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c3*self.r**6) + self.sq3*xi**6*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) - self.sq3*xi**6*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) + self.sq3*xi**8*(l2 - l3)*(-3*l1 + 6*l2 - 3*l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c2*self.r**8) - self.sq3*xi**8*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c2*self.r**8) + self.sq3*xi**8*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c2*self.r**8) + self.sq3*xi**10*(l2 - l3)*(-4*l1 + 8*l2 - 4*l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c1*self.r**10) - self.sq3*xi**10*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10) + self.sq3*xi**10*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10),
                xi/(3*self.r) + xi**3*(-l1 + 2*l2 - l3)*(4*l1 - 2*l2 - 2*l3)/(self.c9*self.r**3) - 2*xi**3*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c9*self.r**3) - xi**5*(-2*l1 + 4*l2 - 2*l3)*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c8*self.r**5) + 2*xi**5*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c8*self.r**5) + xi**7*(-3*l1 + 6*l2 - 3*l3)*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c7*self.r**7) - 4*xi**7*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c7*self.r**7) - xi**9*(-4*l1 + 8*l2 - 4*l3)*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c6*self.r**9) + 2*xi**9*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c6*self.r**9),
            ],
            [
                self.sq3*xi**2*(l2 - l3)/(self.c5*self.r**2) - self.sq3*xi**2*(2*l1 - l2 - l3)/(self.c5*self.r**2) + self.sq3*xi**4*(l2 - l3)*(-l1 + 2*l2 - l3)*(2*l1 - l2 - l3)/(self.c4*self.r**4) - self.sq3*xi**4*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c4*self.r**4) + self.sq3*xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c4*self.r**4) - self.sq3*xi**6*(l2 - l3)*(-2*l1 + 4*l2 - 2*l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c3*self.r**6) + self.sq3*xi**6*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) - self.sq3*xi**6*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) + self.sq3*xi**8*(l2 - l3)*(-3*l1 + 6*l2 - 3*l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c2*self.r**8) - self.sq3*xi**8*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c2*self.r**8) + self.sq3*xi**8*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c2*self.r**8) + self.sq3*xi**10*(l2 - l3)*(-4*l1 + 8*l2 - 4*l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c1*self.r**10) - self.sq3*xi**10*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10) + self.sq3*xi**10*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10),
                -xi**2*(2*l2 - 2*l3)/(6*self.r**2) + xi**4*(l2 - l3)**2*(-l1 + 2*l2 - l3)/(self.c13*self.r**4) + xi**4*(2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c13*self.r**4) - xi**6*(l2 - l3)**2*(-2*l1 + 4*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c12*self.r**6) - xi**6*(2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c12*self.r**6) + xi**8*(l2 - l3)**2*(-3*l1 + 6*l2 - 3*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c11*self.r**8) + xi**8*(2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c11*self.r**8) - xi**10*(l2 - l3)**2*(-4*l1 + 8*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c10*self.r**10) - xi**10*(2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c10*self.r**10),
                -self.sq3*xi/(3*self.r) + 2*self.sq3*xi**3*(l2 - l3)*(-l1 + 2*l2 - l3)/(self.c9*self.r**3) + 2*self.sq3*xi**3*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c9*self.r**3) - 2*self.sq3*xi**5*(l2 - l3)*(-2*l1 + 4*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c8*self.r**5) - 2*self.sq3*xi**5*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c8*self.r**5) + 4*self.sq3*xi**7*(l2 - l3)*(-3*l1 + 6*l2 - 3*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c7*self.r**7) + 4*self.sq3*xi**7*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c7*self.r**7) - 2*self.sq3*xi**9*(l2 - l3)*(-4*l1 + 8*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c6*self.r**9) - 2*self.sq3*xi**9*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c6*self.r**9),
            ], 
            [
                -xi/(3*self.r) - xi**3*(-l1 + 2*l2 - l3)*(4*l1 - 2*l2 - 2*l3)/(self.c9*self.r**3) + 2*xi**3*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c9*self.r**3) + xi**5*(-2*l1 + 4*l2 - 2*l3)*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c8*self.r**5) - 2*xi**5*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c8*self.r**5) - xi**7*(-3*l1 + 6*l2 - 3*l3)*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c7*self.r**7) + 4*xi**7*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c7*self.r**7) + xi**9*(-4*l1 + 8*l2 - 4*l3)*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c6*self.r**9) - 2*xi**9*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c6*self.r**9),
                self.sq3*xi/(3*self.r) - 2*self.sq3*xi**3*(l2 - l3)*(-l1 + 2*l2 - l3)/(self.c9*self.r**3) - 2*self.sq3*xi**3*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c9*self.r**3) + 2*self.sq3*xi**5*(l2 - l3)*(-2*l1 + 4*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c8*self.r**5) + 2*self.sq3*xi**5*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c8*self.r**5) - 4*self.sq3*xi**7*(l2 - l3)*(-3*l1 + 6*l2 - 3*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c7*self.r**7) - 4*self.sq3*xi**7*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c7*self.r**7) + 2*self.sq3*xi**9*(l2 - l3)*(-4*l1 + 8*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c6*self.r**9) + 2*self.sq3*xi**9*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c6*self.r**9),
                -2*xi**2*(-l1 + 2*l2 - l3)/(9*self.r**2) - 4*xi**6*(-3*l1 + 6*l2 - 3*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) + 2*xi**8*(-4*l1 + 8*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c15*self.r**8) + 2*xi**4*(-2*l1 + 4*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c14*self.r**4) - 4*xi**10*(-5*l1 + 10*l2 - 5*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10)
            ]
        ])

    def linearized_dRdl3(self, q, xi):
        l1 = q[0,0]
        l2 = q[1,0]
        l3 = q[2,0]
        return np.array([
            [
                -xi**2*(-4*l1 + 2*l2 + 2*l3)/(self.c5*self.r**2) + xi**4*(-4*l1 + 2*l2 + 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c4*self.r**4) + xi**4*(-l1 - l2 + 2*l3)*(2*l1 - l2 - l3)**2/(self.c4*self.r**4) - xi**6*(-4*l1 + 2*l2 + 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) - xi**6*(-2*l1 - 2*l2 + 4*l3)*(2*l1 - l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c3*self.r**6) + xi**8*(-4*l1 + 2*l2 + 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c1*self.r**8) + xi**8*(-3*l1 - 3*l2 + 6*l3)*(2*l1 - l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c1*self.r**8) - xi**10*(-4*l1 - 4*l2 + 8*l3)*(2*l1 - l2 - l3)**2*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c1*self.r**10) - xi**10*(-4*l1 + 2*l2 + 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10),
                self.sq3*xi**2*(l2 - l3)/(self.c5*self.r**2) + self.sq3*xi**2*(2*l1 - l2 - l3)/(self.c5*self.r**2) + self.sq3*xi**4*(l2 - l3)*(-l1 - l2 + 2*l3)*(2*l1 - l2 - l3)/(self.c4*self.r**4) - self.sq3*xi**4*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c4*self.r**4) - self.sq3*xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c4*self.r**4) - self.sq3*xi**6*(l2 - l3)*(-2*l1 - 2*l2 + 4*l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c3*self.r**6) + self.sq3*xi**6*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) + self.sq3*xi**6*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) + self.sq3*xi**8*(l2 - l3)*(-3*l1 - 3*l2 + 6*l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c2*self.r**8) - self.sq3*xi**8*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c2*self.r**8) - self.sq3*xi**8*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c2*self.r**8) + self.sq3*xi**10*(l2 - l3)*(-4*l1 - 4*l2 + 8*l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c1*self.r**10) - self.sq3*xi**10*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10) - self.sq3*xi**10*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10),
                xi/(3*self.r) + xi**3*(-l1 - l2 + 2*l3)*(4*l1 - 2*l2 - 2*l3)/(self.c9*self.r**3) - 2*xi**3*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c9*self.r**3) - xi**5*(-2*l1 - 2*l2 + 4*l3)*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c8*self.r**5) + 2*xi**5*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c8*self.r**5) + xi**7*(-3*l1 - 3*l2 + 6*l3)*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c7*self.r**7) - 4*xi**7*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c7*self.r**7) - xi**9*(-4*l1 - 4*l2 + 8*l3)*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c6*self.r**9) + 2*xi**9*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c6*self.r**9)
            ],
            [
                self.sq3*xi**2*(l2 - l3)/(self.c5*self.r**2) + self.sq3*xi**2*(2*l1 - l2 - l3)/(self.c5*self.r**2) + self.sq3*xi**4*(l2 - l3)*(-l1 - l2 + 2*l3)*(2*l1 - l2 - l3)/(self.c4*self.r**4) - self.sq3*xi**4*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c4*self.r**4) - self.sq3*xi**4*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c4*self.r**4) - self.sq3*xi**6*(l2 - l3)*(-2*l1 - 2*l2 + 4*l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c3*self.r**6) + self.sq3*xi**6*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) + self.sq3*xi**6*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) + self.sq3*xi**8*(l2 - l3)*(-3*l1 - 3*l2 + 6*l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c2*self.r**8) - self.sq3*xi**8*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c2*self.r**8) - self.sq3*xi**8*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c2*self.r**8) + self.sq3*xi**10*(l2 - l3)*(-4*l1 - 4*l2 + 8*l3)*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c1*self.r**10) - self.sq3*xi**10*(l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10) - self.sq3*xi**10*(2*l1 - l2 - l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10),
                -xi**2*(-2*l2 + 2*l3)/(6*self.r**2) + xi**4*(-2*l2 + 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c13*self.r**4) + xi**4*(l2 - l3)**2*(-l1 - l2 + 2*l3)/(self.c13*self.r**4) - xi**6*(-2*l2 + 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c12*self.r**6) - xi**6*(l2 - l3)**2*(-2*l1 - 2*l2 + 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c12*self.r**6) + xi**8*(-2*l2 + 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c11*self.r**8) + xi**8*(l2 - l3)**2*(-3*l1 - 3*l2 + 6*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c11*self.r**8) - xi**10*(-2*l2 + 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c10*self.r**10) - xi**10*(l2 - l3)**2*(-4*l1 - 4*l2 + 8*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c10*self.r**10),
                self.sq3*xi/(3*self.r) + 2*self.sq3*xi**3*(l2 - l3)*(-l1 - l2 + 2*l3)/(self.c9*self.r**3) - 2*self.sq3*xi**3*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c9*self.r**3) - 2*self.sq3*xi**5*(l2 - l3)*(-2*l1 - 2*l2 + 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c8*self.r**5) + 2*self.sq3*xi**5*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c8*self.r**5) + 4*self.sq3*xi**7*(l2 - l3)*(-3*l1 - 3*l2 + 6*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c7*self.r**7) - 4*self.sq3*xi**7*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c7*self.r**7) - 2*self.sq3*xi**9*(l2 - l3)*(-4*l1 - 4*l2 + 8*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c6*self.r**9) + 2*self.sq3*xi**9*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c6*self.r**9)], 
            [
                -xi/(3*self.r) - xi**3*(-l1 - l2 + 2*l3)*(4*l1 - 2*l2 - 2*l3)/(self.c9*self.r**3) + 2*xi**3*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c9*self.r**3) + xi**5*(-2*l1 - 2*l2 + 4*l3)*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c8*self.r**5) - 2*xi**5*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c8*self.r**5) - xi**7*(-3*l1 - 3*l2 + 6*l3)*(8*l1 - 4*l2 - 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c7*self.r**7) + 4*xi**7*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c7*self.r**7) + xi**9*(-4*l1 - 4*l2 + 8*l3)*(4*l1 - 2*l2 - 2*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c6*self.r**9) - 2*xi**9*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c6*self.r**9), -self.sq3*xi/(3*self.r) - 2*self.sq3*xi**3*(l2 - l3)*(-l1 - l2 + 2*l3)/(self.c9*self.r**3) + 2*self.sq3*xi**3*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c9*self.r**3) + 2*self.sq3*xi**5*(l2 - l3)*(-2*l1 - 2*l2 + 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c8*self.r**5) - 2*self.sq3*xi**5*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c8*self.r**5) - 4*self.sq3*xi**7*(l2 - l3)*(-3*l1 - 3*l2 + 6*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c7*self.r**7) + 4*self.sq3*xi**7*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c7*self.r**7) + 2*self.sq3*xi**9*(l2 - l3)*(-4*l1 - 4*l2 + 8*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c6*self.r**9) - 2*self.sq3*xi**9*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c6*self.r**9),
                -2*xi**2*(-l1 - l2 + 2*l3)/(9*self.r**2) - 4*xi**6*(-3*l1 - 3*l2 + 6*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**2/(self.c3*self.r**6) + 2*xi**8*(-4*l1 - 4*l2 + 8*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**3/(self.c15*self.r**8) + 2*xi**4*(-2*l1 - 2*l2 + 4*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)/(self.c14*self.r**4) - 4*xi**10*(-5*l1 - 5*l2 + 10*l3)*(l1**2 - l1*l2 - l1*l3 + l2**2 - l2*l3 + l3**2)**4/(self.c1*self.r**10)
            ]
        ])


class KinematicsOfHole:
    """アーム全体の運動学"""
    
    def __init__(self,):
        pass


if __name__ == "__main__":
    hoge = KinematicsOfOneSection()
    q = np.array([[1,2,3]]).T
    print(hoge.linearized_dRdl1(q,1))
    print(hoge.linearized_dRdl2(q,1))
    print(hoge.linearized_dRdl3(q,1))