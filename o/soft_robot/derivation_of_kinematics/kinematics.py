"""運動学"""

import sympy as sy
from sympy import sqrt

#import utils



class Local:
    """ローカル座標系関連  
    
    全セクションで同一のパラメータであると仮定  
    """

    # モーダル同時変換行列のパラメータ
    c1 = 837019575
    c2 = 4133430
    c3 = 32805
    c4 = 486
    c5 = 18
    c6 = 55801305
    c7 = 688905
    c8 = 3645
    c9 = 81
    
    c10 = 279006525
    c11 = 1377810
    c12 = 10935
    c13 = 162

    c14 = 243
    c15 = 2066715

    r = 0.0125
    L0 = 0.15
    
    sq3 = sqrt(3)
    
    
    def As(self, q):
        """Aを計算"""
        l1 = q[0,0]
        l2 = q[1,0]
        l3 = q[2,0]
        A1 = l1**2 + l2**2 + l3**2 - l1*l2 - l1*l3 - l2*l3
        A2 = 2*l1 - l2 - l3
        A3 = l2 - l3
        A4 = 3*self.L0 + l1 + l2 + l3
        return A1, A2, A3, A4
    
    def _P1(self, A1, A2, A3, A4, xi):
        return -(A2 * A1**4 * A4 * xi**10) / ((self.c1 * self.r**9)) + \
            (A2 * A1**3 * A4 * xi**8) / (self.c2 * self.r**7) - \
                (A2 * A1**2 * A4 * xi**6) / (self.c3 * self.r**5) + \
                    (A2 * A1 * A4 * xi**4) / (self.c4 * self.r**3) - \
                        (A2 * A4 * xi**2) / (self.c5 * self.r)
    
    
    def _P2(self, A1, A2, A3, A4, xi):
        return -(self.sq3 * A4 * A3 * A1**4 * xi**10) / (self.c1 * self.r**9) + \
            (self.sq3 * A4 * A3 * A1**3 * xi**8) / (self.c2 * self.r**7) - \
                (self.sq3 * A4 * A3 * A1**2 * xi**6) / (self.c3 * self.r**5) + \
                    (self.sq3 * A4 * A1 * A2 * xi**4) / (self.c4 * self.r**3) - \
                        (self.sq3 * A4 * A3 * xi**2) / (self.c5 * self.r)
    
    
    def _P3(self, A1, A2, A3, A4, xi):
        return (2 * A1**4 * A4 * xi**9) / (self.c6 * self.r**8) - \
            (4 * A1**3 * A4 * xi**7) / (self.c7 * self.r**6) + \
                (2 * A1**2 * A4 * xi**5) / (self.c8 * self.r**4) - \
                    (2 * A1 *A4 * xi**3) / (self.c9 * self.r**2) + \
                        (A4 * xi) / 3
    
    
    
    
    def P(self, q, xi):
        """線形化されたアクチュエータ空間からタスク空間への写像
        
        順運動学
        """

        A1, A2, A3, A4 = self.As(q)

        return sy.Matrix([[
            self._P1(A1, A2, A3, A4, xi),
            self._P2(A1, A2, A3, A4, xi),
            self._P3(A1, A2, A3, A4, xi)
        ]]).T
    
    
    def _R11(self, A1, A2, A3, A4, xi):
        return 1 - (A2**2 * A1**4 * xi**10) / (self.c1 * self.r**10) + \
            (A2**2 * A1**3 * xi**8) / (self.c1 * self.r**8) - \
                (A2**2 * A1**2 * xi**6) / (self.c3 * self.r**6) + \
                    (A1 * A2**2 * xi**4) / (self.c4 * self.r**4) - \
                        (A2**2 * xi**2) / (self.c5 * self.r**2)

    def _R12(self, A1, A2, A3, A4, xi):
        return (self.sq3 * A2 * A3 * A1**4 * xi**10) / (self.c1 * self.r**10) + \
            (self.sq3 * A2 * A3 * A1**3 * xi**8) / (self.c2 * self.r**8) - \
                (self.sq3 * A2 * A3 * A1**2 * xi**6) / (self.c3 * self.r**6) + \
                    (self.sq3 * A2 * A3 * A1 * xi**4) / (self.c4 * self.r**4) - \
                        (self.sq3 * A2 * A3 * xi**2) / (self.c5 * self.r**2)

    def _R13(self, A1, A2, A3, A4, xi):
        return -(2 * A2 * A1**4 * xi**9) / (self.c6 * self.r**9) + \
            (4 * A2 * A1**3 * xi**7) / (self.c7 * self.r**7) - \
                (2 * A2 * A1**2 * xi**5) / (self.c8 * self.r**5) + \
                    (2 * A2 * A1 * xi**3) / (self.c9 * self.r**3) - \
                        (A2 * xi) / (3 * self.r)

    def _R21(self, A1, A2, A3, A4, xi):
        return self._R12(A1, A2, A3, A4, xi)

    def _R22(self, A1, A2, A3, A4, xi):
        return 1 - (A3**2 * A1**4 * xi**10) / (self.c10 * self.r**10) + \
            (A3**2 * A1**3 * xi**8) / (self.c11 * self.r**8) - \
                (A3**2 * A1**2 * xi**6) / (self.c12 * self.r**6) + \
                    (A3**2 * A1 * xi**4) / (self.c13 * self.r**4) - \
                        (A3**2 * xi**2) / (6 * self.r**2)

    def _R23(self, A1, A2, A3, A4, xi):
        return -(2*self.sq3 * A3 * A1**4 * xi**9) / (self.c6 * self.r**9) + \
            (4*self.sq3 * A3 * A1**3 * xi**7) / (self.c7 * self.r**7) - \
                (2*self.sq3 * A3 * A1**2 * xi**5) / (self.c8 * self.r**5) + \
                    (2*self.sq3 * A3 * A1 * xi**3) / (self.c9 * self.r**3) - \
                        (self.sq3 * A3 * xi) / (3 * self.r)

    def _R31(self, A1, A2, A3, A4, xi):
        return -self._R13(A1, A2, A3, A4, xi)

    def _R32(self, A1, A2, A3, A4, xi):
        return -self._R23(A1, A2, A3, A4, xi)

    def _R33(self, A1, A2, A3, A4, xi):
        return 1 - (2 * xi**2 * A1) / (9 * self.r**2) + \
            (2 * xi**4 * A1**2) / (self.c14 * self.r**4) - \
                (4 * xi**6 * A1**3) / (self.c3 * self.r**6) + \
                    (2 * xi**8 * A1**4) / (self.c15 * self.r**8) - \
                        (4 * xi**10 * A1**5) / (self.c1 * self.r**10)

    def R(self, q, xi):
        """線形化された回転行列"""
        
        A1, A2, A3, A4 = self.As(q)
        
        return sy.Matrix([
            [
                self._R11(A1, A2, A3, A4, xi),
                self._R12(A1, A2, A3, A4, xi),
                self._R13(A1, A2, A3, A4, xi)
            ],
            [
                self._R21(A1, A2, A3, A4, xi),
                self._R22(A1, A2, A3, A4, xi),
                self._R23(A1, A2, A3, A4, xi)
            ],
            [
                self._R31(A1, A2, A3, A4, xi),
                self._R32(A1, A2, A3, A4, xi),
                self._R33(A1, A2, A3, A4, xi)
            ],
        ])


    def MHTM(self, q, xi):
        """モーダル同時変換行列
        
        線形化されたHomogeneous Transformation Matrix
        """
        A1, A2, A3, A4 = self.As(q)
        
        return sy.Matrix([
            [
                self._R11(A1, A2, A3, A4, xi),
                self._R12(A1, A2, A3, A4, xi),
                self._R13(A1, A2, A3, A4, xi),
                self._P1(A1, A2, A3, A4, xi)
            ],
            [
                self._R21(A1, A2, A3, A4, xi),
                self._R22(A1, A2, A3, A4, xi),
                self._R23(A1, A2, A3, A4, xi),
                self._P2(A1, A2, A3, A4, xi)
            ],
            [
                self._R31(A1, A2, A3, A4, xi),
                self._R32(A1, A2, A3, A4, xi),
                self._R33(A1, A2, A3, A4, xi),
                self._P3(A1, A2, A3, A4, xi)
            ],
            [
                0,
                0,
                0,
                1
            ]
        ])



class Global(Local):
    """位置，回転行列，ヤコビアン，ヘッシアン等のグローバル表現  
    
    全セクションで同一のパラメータであると仮定.   
    すぐ終わる.   
    """
    
    
    def __init__(self, N):
        """
        Parameters  
        ---
        N : int
            セクションの数
        """
        
        
        print("computing kinematics...")
        
        self.N = N
        # self.q_large = q_large
        # self.xi_large = xi_large
        
        self.q_large = sy.Matrix(sy.MatrixSymbol('q_large', 3*N, 1))  # 完全な関節角度ベクトル
        self.q_dot_large = sy.Matrix(sy.MatrixSymbol('q_dot_large', 3*N, 1))  # 完全な関節角速度ベクトル
        self.xi_large = sy.Matrix(sy.MatrixSymbol('xi_large', N, 1))  # 完全なスカラξベクトル
        
        self.set_local()
        self.set_global()
        # self.set_J_OMEGA()
        # self.set_J_v()
        # self.set_H_OMEGA()
        # self.set_H_v()
        
        print("done computing kinematics!")
    
    
    def set_local(self,):
        """ローカル座標系を用意"""
        
        self.P_s = []
        self.R_s = []
        for i in range(self.N):
            print(self.q_large[3*i:3*(i+1), :])
            self.P_s.append(
                self.P(self.q_large[3*i:3*(i+1), :], self.xi_large[i, 0])
            )
            self.R_s.append(
                self.R(self.q_large[3*i:3*(i+1), :], self.xi_large[i, 0])
            )
    
    
    def set_global(self,):
        """グローバル座標系を用意"""
        
        self.Theta_s = []
        self.Phi_s = []
        for i in range(self.N):
            if i == 0:
                self.Theta_s.append(self.R_s[0])
                self.Phi_s.append(self.P_s[0])
            else:
                Theta = self.Theta_s[i-1] * self.R_s[i]
                self.Theta_s.append(Theta.subs(self.xi_large[i-1, 0], 1))
                
                Phi = self.Phi_s[i-1] + self.Theta_s[i-1] * self.P_s[i]
                self.Phi_s.append(Phi.subs(self.xi_large[i-1, 0], 1))


    def set_J_v_simple(self,):
        """各接続位置のヤコビアンをセット（単純に計算）"""
        
        
        self.J_v_simples = []
        for i in range(self.N):
            self.J_v_simples.append(
                self.Phi_s[i].jacobian(self.q_large)
            )
        



    def set_H_v_simple(self,):
        """各接続位置のヘッシアンをセット（単純に計算）"""
        
        
        self.H_v_simples = []
        for i in range(self.N):
            self.H_v_simples.append(
                sy.simplify(
                    sy.hessian(self.Phi_s[i], (self.q_large, self.xi_large), [self.q_large, self.q_large])
                )
            )
        


    def set_J_OMEGA(self,):
        """角速度ヤコビアンのハット変換を計算"""
        
        def J_OMEGA_ij(i, j):
            if j <= 3*i-1:
                return self.R_s[i].T * J_OMEGA_s[i-1][:, 3*j:3*j+3] * self.R_s[i]
            elif 3*i <= j <= 3*i+2:
                return self.R_s[i].T * sy.diff(self.R_s[i], self.q_large[j, 0])
            else:
                return sy.zeros(3, 3)
        
        J_OMEGA_s = []
        for i in range(self.N):
            #print("i = ", i)
            J_OMEGAs_i = []
            for j in range(3*self.N):
                #print("j = ", j)
                J_OMEGAs_i.append(J_OMEGA_ij(i, j))
            J_OMEGA_s.append(sy.Matrix([J_OMEGAs_i]))
        
        self.J_OMEGA_s = J_OMEGA_s


    def set_J_v(self,):
        """線速度ヤコビアンをセット"""
        
        def J_v_ij(i, j):
            if j < 3*i:
                return self.R_s[i].T * \
                    (J_v_s[i-1][:, j:j+1] + (self.J_OMEGA_s[i][:, 3*j:3*j+3] * self.P_s[i]))
            elif 3*i <= j <= 3*i+2:
                return self.R_s[i].T * sy.diff(self.P_s[i], self.q_large[j, 0])
            else:
                return sy.zeros(3, 1)
        
        J_v_s = []
        for i in range(self.N):
            #print("i = ", i)
            J_v_s_i = []
            for j in range(3*self.N):
                #print("j = ", j)
                J_v_s_i.append(J_v_ij(i, j))
            J_v_s.append(sy.Matrix([J_v_s_i]))
        
        self.J_v_s = J_v_s
    
    
    def set_H_OMEGA(self,):
        """角速度ヘッシアンをセット
        
        ※本当はテンソル?  
        """
        
        
        def H_OMEGA_ijk(i, j, k):
            if j < 3*i and k < 3*i:
                H_OMEGA_prev = H_OMEGA_s[i-1][3*j:3*j+3, 3*k:3*k+3]  # テンソルから1枚剥がして持ってくる
                #print(H_OMEGA_prev.shape)
                return self.R_s[i].T * H_OMEGA_prev * self.R_s[i]

            elif j < 3*i and 3*i <= k <= 3*i+2:
                R_i_diff_k = sy.diff(self.R_s[i], self.q_large[k, 0])
                return R_i_diff_k.T * self.J_OMEGA_s[i-1][:, 3*j:3*j+3] * self.R_s[i] +\
                    self.R_s[i].T * self.J_OMEGA_s[i-1][:, 3*j:3*j+3] * R_i_diff_k
            
            elif 3*i <= j <= 3*i+2 and k < 3*i:
                return sy.zeros(3, 3)
            
            elif 3*i <= j <= 3*i+2 and 3*i <= k <= 3*i+2:
                R_i_diff_k = sy.diff(self.R_s[i], self.q_large[k, 0])
                R_i_diff_j = sy.diff(self.R_s[i], self.q_large[j, 0])
                R_i_diff_j_diff_k = sy.diff(R_i_diff_j, self.q_large[k, 0])
                return R_i_diff_k.T * R_i_diff_j + self.R_s[i].T * R_i_diff_j_diff_k
            
            else:
                return sy.zeros(3, 3)
        
        
        H_OMEGA_s = []
        for i in range(self.N):
            #print("i = ", i)
            H_OMEGA_s_i = []
            
            for j in range(3*self.N):
                #print("j = ", j)
                H_OMEGA_s_ij = []
                
                for k in range(3*self.N):
                    #print("k = ", k)
                    H_OMEGA_s_ij.append(H_OMEGA_ijk(i, j, k))
                H_OMEGA_s_i.append([sy.Matrix([H_OMEGA_s_ij])])
            
            H_OMEGA_s.append(sy.Matrix(H_OMEGA_s_i))
            #print(H_OMEGA_s[-1].shape)
        
        
        self.H_OMEGA_s = H_OMEGA_s
    
    
    def set_H_v(self,):
        """線速度ヘッシアンをセット
        
        ホントはテンソル?  
        """
        
        def H_v_ijk(i, j, k):
            if j < 3*i and k < 3*i:
                return self.R_s[i].T * \
                    (H_v_s[i-1][3*j:3*j+3, k:k+1] + self.H_OMEGA_s[i-1][3*j:3*j+3, 3*k:3*k+3] * self.P_s[i])
            
            elif j < 3*i and 3*i <= k <= 3*i+2:
                R_i_diff_k = sy.diff(self.R_s[i], self.q_large[k, 0])
                P_i_diff_k = sy.diff(self.P_s[i], self.q_large[k, 0])
                return R_i_diff_k.T *\
                    (self.J_v_s[i-1][:, j:j+1] + self.J_OMEGA_s[i-1][:, 3*j:3*j+3] * self.P_s[i]) +\
                        self.R_s[i].T * self.J_OMEGA_s[i][:, 3*j:3*j+3] * P_i_diff_k
            
            elif 3*i <= j <= 3*i+2 and k < 3*i:
                return sy.zeros(3, 1)
            
            elif 3*i <= j <= 3*i+2 and 3*i <= k <= 3*i+2:
                R_i_diff_k = sy.diff(self.R_s[i], self.q_large[k, 0])
                P_i_diff_j = sy.diff(self.P_s[i], self.q_large[j, 0])
                P_i_diff_j_diff_k = sy.diff(P_i_diff_j, self.q_large[k, 0])
                return R_i_diff_k.T * P_i_diff_j + self.R_s[i].T * P_i_diff_j_diff_k
            
            else:
                return sy.zeros(3, 1)
        
        
        H_v_s = []
        for i in range(self.N):
            #print("i = ", i)
            H_v_s_i = []
            
            for j in range(3*self.N):
                #print("j = ", j)
                H_v_s_ij = []
                
                for k in range(3*self.N):
                    #print("k = ", k)
                    H_v_s_ij.append(H_v_ijk(i, j, k))
                H_v_s_i.append([sy.Matrix([H_v_s_ij])])
            
            H_v_s.append(sy.Matrix(H_v_s_i))
            #print(H_OMEGA_s[-1].shape)
        
        
        self.H_v_s = H_v_s




if __name__ == "__main__":
    

    N = 3

    
    hoge = Global(
        # sy.Matrix(q_large), 
        # sy.Matrix(xi_large),
        N
    )
    #print(hoge.J_v_s)
    
    
    hoge.set_J_v_simple()
