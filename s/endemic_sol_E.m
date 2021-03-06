function out1 = endemic_sol_E(ALPHA,CONTACT_E,CONTACT_I,CONTACT_S1,GAMMA,MU,RATE_W,SPAN1,SPAN2,SPAN12,THETA1,THETA2,TOTAL)
%ENDEMIC_SOL_E
%    OUT1 = ENDEMIC_SOL_E(ALPHA,CONTACT_E,CONTACT_I,CONTACT_S1,GAMMA,MU,RATE_W,SPAN1,SPAN2,SPAN12,THETA1,THETA2,TOTAL)

%    This function was generated by the Symbolic Math Toolbox version 8.6.
%    23-Dec-2021 15:24:12

t2 = MU.^2;
t3 = TOTAL.^2;
out1 = [0.0;-((GAMMA+MU+RATE_W).*(CONTACT_E.*TOTAL.*t2+ALPHA.*CONTACT_I.*MU.*TOTAL+CONTACT_E.*GAMMA.*MU.*TOTAL+CONTACT_E.*MU.*RATE_W.*TOTAL-SPAN1.*THETA1.*t2.*t3-ALPHA.*GAMMA.*SPAN1.*THETA1.*t3-ALPHA.*MU.*SPAN1.*THETA1.*t3-ALPHA.*RATE_W.*SPAN1.*THETA1.*t3-GAMMA.*MU.*SPAN1.*THETA1.*t3-MU.*RATE_W.*SPAN1.*THETA1.*t3+ALPHA.*CONTACT_S1.*SPAN1.*THETA1.*TOTAL+CONTACT_S1.*GAMMA.*SPAN1.*THETA1.*TOTAL+CONTACT_S1.*MU.*SPAN1.*THETA1.*TOTAL+CONTACT_S1.*RATE_W.*SPAN1.*THETA1.*TOTAL+ALPHA.*CONTACT_I.*SPAN2.*SPAN12.*THETA2.*TOTAL+CONTACT_E.*GAMMA.*SPAN2.*SPAN12.*THETA2.*TOTAL+CONTACT_E.*MU.*SPAN2.*SPAN12.*THETA2.*TOTAL+CONTACT_E.*RATE_W.*SPAN2.*SPAN12.*THETA2.*TOTAL))./(CONTACT_E.*CONTACT_S1.*t2+ALPHA.^2.*CONTACT_I.*CONTACT_S1+CONTACT_E.*CONTACT_S1.*GAMMA.^2+CONTACT_E.*CONTACT_S1.*RATE_W.^2+ALPHA.*CONTACT_E.*CONTACT_S1.*GAMMA+ALPHA.*CONTACT_I.*CONTACT_S1.*GAMMA+ALPHA.*CONTACT_E.*CONTACT_S1.*MU+ALPHA.*CONTACT_I.*CONTACT_S1.*MU+ALPHA.*CONTACT_E.*CONTACT_S1.*RATE_W+ALPHA.*CONTACT_I.*CONTACT_S1.*RATE_W+CONTACT_E.*CONTACT_S1.*GAMMA.*MU.*2.0+CONTACT_E.*CONTACT_S1.*GAMMA.*RATE_W.*2.0+CONTACT_E.*CONTACT_S1.*MU.*RATE_W.*2.0)];
