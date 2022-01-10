"""シミュレーション"""


using LinearAlgebra
using Plots
using ProgressBars
using Parameters
using DifferentialEquations


include("kinematics.jl")
include("dynamics.jl")
include("controller.jl")
include("plot_utils.jl")

using .Kinematics: Phi0, Arm
using .Dynamics: H_dot, calc_q_dot_dot
using .Controller




"""シミュレーションのデータを格納"""
@with_kw struct Data{T}
    t::Vector{T}
    q::Vector{Vector{T}}
    q_dot::Vector{Vector{T}}
    q_dot_dot::Vector{Vector{T}}
    qd::Vector{Vector{T}}
    qd_dot::Vector{Vector{T}}
    qd_dot_dot::Vector{Vector{T}}
    τ::Vector{Vector{T}}
    error::Vector{Vector{T}}
end

const R = 0.01

"""適当な目標アクチュエータ変位"""
function calc_qd(t::T) where T
    [
        R * sin(3t),
        R * sin(3t + π/2),
        R * sin(3t + π),
    ]
end


"""適当な目標アクチュエータ速度"""
function calc_qd_dot(t::T) where T
    [
        R * 3cos(3t),
        R * 3cos(3t + π/2),
        R * 3cos(3t + π),
    ]
end


"""適当な目標アクチュエータ加速度"""
function calc_qd_dot_dot(t::T) where T
    [
        R * -9sin(3t),
        R * -9sin(3t + π/2),
        R * -9sin(3t + π),
    ]
end


"""状態方程式"""
function X_dot(X::Vector{T}, τ::Vector{T}) where T
    q = X[1:3]
    q_dot = X[4:6]
    H = X[7:9]


    x1_dot = q_dot
    x2_dot = calc_q_dot_dot(τ, q, q_dot, H)
    x3_dot = H_dot(H, q, q_dot)


    #println(norm([x1_dot; x2_dot]))
    return [x1_dot; x2_dot; x3_dot]

end


"""シミュレーション実行

自分で書いたオイラー法．遅い.
"""
function run_simulation(;TIME_SPAN::T=2.2π/3, Δt::T=0.0001) where T


    # 制御器のパラメータ
    kinematic = KinematicController(Dynamics.K)
    PDandFL = PDandFBController(
        Matrix{Float64}(I, 3, 3)*200, Matrix{Float64}(I, 3, 3)*1500
    )
    passivity = PassiveController(
        Matrix{Float64}(I, 3, 3)*100, Matrix{Float64}(I, 3, 3)*10,
    )




    q₀ = zeros(T, 3)
    q_dot₀ = zeros(T, 3)
    H₀ = zeros(T, 3)  # ヒステリシスベクトル

    t = Vector(0.0:Δt:TIME_SPAN)

    data = Data(
        t = t,
        q = Vector{typeof(q₀)}(undef, length(t)),
        q_dot = Vector{typeof(q₀)}(undef, length(t)),
        q_dot_dot = Vector{typeof(q₀)}(undef, length(t)),
        qd = Vector{typeof(q₀)}(undef, length(t)),
        qd_dot = Vector{typeof(q₀)}(undef, length(t)),
        qd_dot_dot = Vector{typeof(q₀)}(undef, length(t)),
        τ = Vector{typeof(q₀)}(undef, length(t)),
        error = Vector{typeof(q₀)}(undef, length(t)),
    )

    # 初期値代入
    data.q[1] = q₀
    data.q_dot[1] = q_dot₀
    data.q_dot_dot[1] = zeros(T, 3)
    data.qd[1] = calc_qd(t[1])
    data.qd_dot[1] = calc_qd_dot(t[1])
    data.qd_dot_dot[1] = calc_qd_dot_dot(t[1])
    data.τ[1] = zeros(T, 3)
    data.error[1] = data.qd[1] .- data.q[1]
    H = H₀


    # メインループ
    for i in tqdm(1:length(t)-1)

        # ルンゲクッタの部分
        X = [data.q[i]; data.q_dot[i]; H]
        k₁ = X_dot(X, data.τ[i])
        k₂ = X_dot(X.+k₁.*Δt/2, data.τ[i])
        k₃ = X_dot(X.+k₂.*Δt/2, data.τ[i])
        k₄ = X_dot(X.+k₃.*Δt, data.τ[i])
        @. X += (k₁ + 2k₂ + 2k₃ +k₄) * Δt/6

        data.q[i+1] = X[1:3]
        data.q_dot[i+1] = X[4:6]
        H = X[7:9]

        data.q_dot_dot[i+1] = calc_q_dot_dot(
            data.τ[i], data.q[i+1], data.q_dot[i+1], H
        )

        
        data.qd[i+1] = calc_qd(t[i+1])
        data.qd_dot[i+1] = calc_qd_dot(t[i+1])
        data.qd_dot_dot[i+1] = calc_qd_dot_dot(t[i+1])
        data.error[i+1] = data.qd[i+1] .- data.q[i+1]
        
        #data.τ[i+1] = calc_torque(kinematic, data.q[i+1], data.qd[i+1])
        #data.τ[i+1] = calc_torque(PDandFL, data.q[i+1], data.q_dot[i+1], data.qd[i+1], data.qd_dot[i+1], data.qd_dot_dot[i+1])
        data.τ[i+1] = calc_torque(passivity, data.q[i+1], data.q_dot[i+1], data.qd[i+1], data.qd_dot[i+1], data.qd_dot_dot[i+1])
    end

    data
end


"""ソルバで使うやつ"""
function state_eq!(X_dot::Vector{T}, X::Vector{T}, p, t::T) where T
    q = X[1:3]
    q_dot = X[4:6]
    H = X[7:9]

    τ = calc_torque(
    p, q, q_dot,
        calc_qd(t), calc_qd_dot(t), calc_qd_dot_dot(t)
    )

    X_dot[1:3] = q_dot
    X_dot[4:6] = calc_q_dot_dot(τ, q, q_dot, H)
    X_dot[7:9] = H_dot(H, q, q_dot)

end


"""ソルバ使用"""
function run_simulation(;TIME_SPAN::T=1.0, method) where T

    X₀ = zeros(T, 9)
    t_span = (0.0, TIME_SPAN)
    p = PDandFBController(
        Matrix{Float64}(I, 3, 3)*200, Matrix{Float64}(I, 3, 3)*1500
    )
    prob = ODEProblem(state_eq!, X₀, t_span, p)
    sol = solve(prob)
    
    plot(
        sol,
        label=["l1" "l2" "l3" "l1_dot" "l2_dot" "l3_dot" "h1" "h2" "h3"],
        )

end


# @time data = run_simulation(TIME_SPAN=0.01)
# @time make_plot_basic(data)
# @time make_animation(data)



@time run_simulation(TIME_SPAN=2.2π/3, method=nothing)