module C1_1
function f(q::Vector{T}, q_dot::Vector{T}, xi::T) where T
    l1 = q[1]
    l2 = q[2]
    l3 = q[3]
    l1_dot = q_dot[1]
    l2_dot = q_dot[2]
    l3_dot = q_dot[3]
    
    l1_dot.*(7.00120879963642e-11*l1 - 4.28998384220961e-11*l2 - 2.75081888864459e-11*l3 + 6.01947273729361e-14) - l2_dot.*(4.28998384220961e-11*l1 - 5.44544999423272e-11*l2 + 1.12667056568291e-11*l3 + 4.41800310108094e-14) - l3_dot.*(6.17485674830662e-12*l1 + 4.31447849383884e-11*l2 - 4.92763081818322e-11*l3 - 6.44040569580091e-15)
end
end