module Phi0
function f(q::Vector{T}, q_dot::Vector{T}, xi::T) where T
    l1 = q[1]
    l2 = q[2]
    l3 = q[3]
    l1_dot = q_dot[1]
    l2_dot = q_dot[2]
    l3_dot = q_dot[3]
    
    [-4.42055412371134e-10*xi.^2.*(0.5*l1 - 5.0e-5).*(l2 - 0.002) - 1.65770779639175e-10*xi.^2.*(0.5*l1 - 5.0e-5).*(l3 - 0.0015) + 1.51956548002578e-10*xi.^2.*(l1 - 0.0001).^2 + 1.20560567010309e-10*xi.^2.*(0.5*l2 - 0.001).*(l3 - 0.0015) + 8.0373711340206e-11*xi.^2.*(l2 - 0.002).^2 + 1.13025531572165e-11*xi.^2.*(l3 - 0.0015).^2, 1.16009459695093e-10*xi.^2.*(0.5*l1 - 5.0e-5).*(l2 - 0.002) + 4.35035473856599e-11*xi.^2.*(0.5*l1 - 5.0e-5).*(l3 - 0.0015) - 3.98782517701883e-11*xi.^2.*(l1 - 0.0001).^2 - 3.16389435532073e-11*xi.^2.*(0.5*l2 - 0.001).*(l3 - 0.0015) - 2.10926290354715e-11*xi.^2.*(l2 - 0.002).^2 - 2.96615095811319e-12*xi.^2.*(l3 - 0.0015).^2, -5.58213595360825e-5*xi.*(0.5*l1 - 5.0e-5).*(l2 - 0.002) - 3.58060567010309e-5*xi.*(0.5*l1 - 5.0e-5).*(l3 - 0.0015) + 2.27779478092784e-5*xi.*(l1 - 0.0001).^2 - 3.898125e-8*xi.*(l1 - 0.0001) - 1.46850837628866e-5*xi.*(0.5*l2 - 0.001).*(l3 - 0.0015) + 1.77203608247422e-5*xi.*(l2 - 0.002).^2 + 2.835e-8*xi.*(l2 - 0.002) + 1.26579413659794e-5*xi.*(l3 - 0.0015).^2 + 1.063125e-8*xi.*(l3 - 0.0015)]
end
end