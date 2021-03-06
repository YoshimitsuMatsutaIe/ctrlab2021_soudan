module M1_1
function f(q::Vector{T}, q_dot::Vector{T}, xi::T) where T
    l1 = q[1]
    l2 = q[2]
    l3 = q[3]
    l1_dot = q_dot[1]
    l2_dot = q_dot[2]
    l3_dot = q_dot[3]
    
    3.38058845865336e-11*l1.^2 - 8.57996768441923e-11*l1.*l2 + 1.77343591248946e-11*l1.*l3 + 6.96600978936586e-14*l1 + 5.44544999423272e-11*l2.^2 - 2.25334113136583e-11*l2.*l3 - 8.83600620216189e-14*l2 + 2.33986794159514e-12*l3.^2 + 1.82331574873355e-14*l3 + 3.59116069801844e-17
end
end