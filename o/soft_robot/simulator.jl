"""シミュレーション"""


using LinearAlgebra  # 逆行列とノルムの計算に使用
using Plots  # グラフ作成
#using ProgressBars
#using Parameters
using DifferentialEquations  # 微分方程式のソルバ
#using LaTeXStrings


include("kinematics.jl")
include("dynamics.jl")
include("controller.jl")
include("plot_utils.jl")

using .Kinematics: Phi0, Arm
using .Dynamics: H_dot, calc_q_dot_dot, uncertain_K, uncertain_D
using .Controller



const R = 0.015

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



"""ソルバで使うやつ"""
function state_eq!(
    X_dot::Vector{T}, X::Vector{T},
    p,
    t::T
    ) where T
    q = X[1:3]
    q_dot = X[4:6]
    H = X[7:9]
    #println(t)
    τ = calc_torque(
    p, q, q_dot,
    calc_qd(t), calc_qd_dot(t), calc_qd_dot_dot(t),
    )
    X_dot[1:3] = q_dot
    X_dot[4:6] = calc_q_dot_dot(τ, q, q_dot, H)
    X_dot[7:9] = H_dot(H, q, q_dot)
end


"""ソルバで使うやつ

受動性に基づく適応制御
"""
function state_eq!(
    X_dot::Vector{T}, X::Vector{T},
    p::PassivityBasedAdaptiveController{T},
    t::T
    ) where T
    q = X[1:3]
    q_dot = X[4:6]
    H = X[7:9]
    θp = X[10:15]  # パラメータの推定値

    #println(t)
    #println(θp)
    τ = calc_torque(
    p, q, q_dot,
    calc_qd(t), calc_qd_dot(t),
    θp
    )
    X_dot[1:3] = q_dot
    X_dot[4:6] = calc_q_dot_dot(τ, q, q_dot, H)
    X_dot[7:9] = H_dot(H, q, q_dot)
    X_dot[10:15] = θp_dot(p, q, q_dot, calc_qd(t), calc_qd_dot(t))
end


"""微分方程式を解く"""
function run_simulation(
    TIME_SPAN::T, method_name::String, controller_param
    ) where T

    X₀ = zeros(T, 9)
    t_span = (0.0, TIME_SPAN) 
    println(method_name * " now...")
    prob = ODEProblem(state_eq!, X₀, t_span, controller_param)
    sol = solve(prob)
    
    return sol
end


"""微分方程式を解く"""
function run_simulation(
    TIME_SPAN::T, method_name::String,
    controller_param::PassivityBasedAdaptiveController{T}
    ) where T

    X₀ = [
        zeros(T, 9); diag(uncertain_K); diag(uncertain_D)
    ]
    t_span = (0.0, TIME_SPAN) 
    println(method_name * " now...")
    prob = ODEProblem(state_eq!, X₀, t_span, controller_param)
    sol = solve(prob)
    
    return sol
end



function reproduce_τ(p::PassivityBasedAdaptiveController{T}, t::T, u::Vector{T}) where T
    calc_torque(
        p, u[1:3], u[4:6],
        calc_qd(t), calc_qd_dot(t),
        u[10:15]
    )
end


function reproduce_τ(p, t::T, u::Vector{T}) where T
    calc_torque(
        p, u[1:3], u[4:6],
        calc_qd(t), calc_qd_dot(t), calc_qd_dot_dot(t),
    )
end

"""実行"""
function exmample()

    TIME_SPAN = 2.0

    hutashikasa = true

    params = (
        # (
        #     name = "kine",
        #     p = KinematicController(
        #         K_kin = Dynamics.K,
        #         isUncertainty = hutashikasa,
        #     ),
        #     marker = :solid,
        # ),
        (
            name = "pdfb",
            p = PDandFBController(
                Kd = Matrix{Float64}(I, 3, 3)*200,
                Kp = Matrix{Float64}(I, 3, 3)*10000,#1500
                isUncertainty = hutashikasa,
            ),
            marker = :dash,
        ),
        # (
        #     name = "psiv",
        #     p = PassivityBasedController(
        #         Λ = Matrix{Float64}(I, 3, 3)*10,
        #         KG = Matrix{Float64}(I, 3, 3)*10,
        #         isUncertainty = hutashikasa,
        #     ),
        #     marker = :dot,
        # ),
        (
            name = "psad",
            p = PassivityBasedAdaptiveController(
                invΓ = Matrix{Float64}(I, 6, 6)*1e+5,
                Λ = Matrix{Float64}(I, 3, 3)*10,
                KG = Matrix{Float64}(I, 3, 3)*10,
                isUncertainty = hutashikasa,
            ),
            marker = :dashdot,
        )
    )
    sols = []
    fig0 = plot(xlims=(0.0, TIME_SPAN))
    fig_tau = plot(xlims=(0.0, TIME_SPAN), ylims=(-150.0, 150.0))
    fig1 = plot(xlims=(0.0, TIME_SPAN))
    fig2 = plot(xlims=(0.0, TIME_SPAN))
    fig3 = plot(xlims=(0.0, TIME_SPAN))
    

    for param in params
        sol = run_simulation(TIME_SPAN, param.name, param.p)
        push!(sols, sol)

        error = Vector{Vector{Float64}}(undef, length(sol.t))
        τ = Vector{Vector{Float64}}(undef, length(sol.t))
        for (i, t) in enumerate(sol.t)
            error[i] = calc_qd(t) .- sol.u[i][1:3]
            τ[i] = reproduce_τ(param.p, t, sol.u[i])
        end
        L2_error = norm.(error)
        plot!(
            fig0,
            sol.t, L2_error,
            label=(param.name * "-") * "err",
            legend=:outerright,
            linestyle=param.marker
        )

        x, y, z = split_vec_of_arrays(τ)
        plot!(fig_tau, sol.t, x, label=param.name*"-"*"τ1_", linestyle=param.marker)
        plot!(fig_tau, sol.t, y, label=param.name*"-"*"τ2_", linestyle=param.marker)
        plot!(fig_tau, sol.t, z, label=param.name*"-"*"τ3_", linestyle=param.marker)
        plot!(fig_tau,legend=:outerright)

        plot!(
            fig1,
            sol, vars=[(0,1), (0,2), (0,3)],
            label=(param.name * "-") .* ["l1_" "l2_" "l3_"],
            legend=:outerright,
            linestyle=param.marker
        )
        plot!(
            fig2,
            sol, vars=[(0,4), (0,5), (0,6)],
            label=(param.name * "-") .* ["dl1" "dl2" "dl3"],
            legend=:outerright,
            linestyle=param.marker
        )
        plot!(
            fig3,
            sol, vars=[(0,7), (0,8), (0,9)],
            label=(param.name * "-") .* ["h1_" "h2_" "h3_"],
            legend=:outerright,
            linestyle=param.marker
        )
    
    end

    fig_I = plot(
        fig0, fig_tau, fig1, fig2, fig3,
        layout=(5,1), size=(500, 1200)
    )
    savefig(fig_I, "solve.png")

    fig_param_K = plot(xlims=(0.0, TIME_SPAN))
    plot!(
        fig_param_K,
        sols[2], vars=[(0,10), (0,11), (0,12)],
        label=["K1" "K2" "K3"],
        legend=:outerright,
    )
    # plot!(
    #     fig_param_K,
    #     [sols[2].t[1], sols[2].t[end]], [Dynamics.K[1], Dynamics.K[1],],
    #     label="real_K"
    # )

    fig_param_D = plot(xlims=(0.0, TIME_SPAN))
    plot!(
        fig_param_D,
        sols[2], vars=[(0,13), (0,14), (0,15)],
        label=["D1" "D2" "D3"],
        legend=:outerright,
    )
    # plot!(
    #     fig_param_D,
    #     [sols[2].t[1], sols[2].t[end]], [Dynamics.D[1], Dynamics.D[1],],
    #     label="real_D"
    # )
    fig_hog = plot(
        fig_param_K, fig_param_D,
        layout=(2,1),
    )
    savefig(fig_hog, "param.png")

    sols
    println("done!")
end


@time sol = exmample()