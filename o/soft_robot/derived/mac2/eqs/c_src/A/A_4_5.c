/******************************************************************************
 *                       Code generated with sympy 1.8                        *
 *                                                                            *
 *              See http://www.sympy.org/ for more information.               *
 *                                                                            *
 *                    This file is part of 'A_4_5project'                     *
 ******************************************************************************/
#include "A_4_5.h"
#include <math.h>

double A_4_5(double l1, double l1_dot, double l2, double l2_dot, double l3, double l3_dot) {

   double A_4_5_result;
   A_4_5_result = ((-5.5165475065185872e-11*pow(l1, 2) + 1.0381797258289777e-10*l1*l2 + 7.1949338249082319e-12*l1*l3 - 1.0428346174204566e-13*l1 - 4.2899838422096126e-11*pow(l2, 2) - 1.8641009323998624e-11*l2*l3 + 9.5024776319765406e-14*l2 + 5.6913216769121215e-12*pow(l3, 2) + 9.8976198705223475e-15*l3 - 4.8930373848445577e-17)*(-3.5367410853738339e-11*pow(l1, 2) + 7.1949338249082319e-12*l1*l2 + 6.3878703884596147e-11*l1*l3 - 5.1905837941352888e-14*l1 + 8.8671795624472777e-12*pow(l2, 2) - 2.4932305151384002e-11*l2*l3 + 7.5507477351706682e-16*l2 - 1.9641886789290257e-11*pow(l3, 2) + 5.1391426246660414e-14*l3 - 1.8509555491132188e-17) - (2.1671405104185884e-11*pow(l1, 2) - 1.8641009323998624e-11*l1*l2 - 2.4932305151384002e-11*l1*l3 + 3.5494223739988346e-14*l1 - 1.1266705656829124e-11*pow(l2, 2) + 4.1222747249460305e-11*l2*l3 - 7.5964125609303015e-15*l2 - 8.0535609323719406e-12*pow(l3, 2) - 2.8073636513462422e-14*l3 + 1.3584774706293312e-17)*(9.0023941147560682e-11*pow(l1, 2) - 1.1033095013037174e-10*l1*l2 - 7.0734821707476691e-11*l1*l3 + 1.5485444573210494e-13*l1 + 3.3805884586533577e-11*pow(l2, 2) + 4.3342810208371768e-11*l2*l3 - 9.4911915884298407e-14*l2 + 1.3896016144405875e-11*pow(l3, 2) - 6.0817043275540881e-14*l3 + 6.6668760917630031e-17))*(l1_dot*(-1.3896016144405882e-11*l1 - 5.6913216769121215e-12*l2 + 1.9641886789290263e-11*l3 - 8.4428838424424756e-15) - l1_dot*(4.9982687740190265e-11*l1 - 3.0623626828296123e-11*l2 - 1.9641886789290253e-11*l3 + 4.2948542404217938e-14) + l2_dot*(-5.6913216769121215e-12*l1 - 2.3398679415951372e-12*l2 + 8.0535609323719406e-12*l3 - 3.448856084669015e-15) + l2_dot*(3.0623626828296123e-11*l1 - 3.8882879307865166e-11*l2 + 8.0535609323719406e-12*l3 + 3.1522492598131435e-14) + 2*l3_dot*(1.964188678929026e-11*l1 + 8.0535609323719406e-12*l2 - 2.7772582237026216e-11*l3 + 1.1924852085787161e-14) - 110)/(-4.0804888099759188e-21*pow(-0.55366512942456425*pow(l1, 2) + 0.11263431139596485*l1*l2 + l1*l3 - 0.00081256874020372194*l1 + 0.13881276580794133*pow(l2, 2) - 0.39030699803219132*l2*l3 + 1.1820446057909876e-5*l2 - 0.30748724684169343*pow(l3, 2) + 0.00080451579511545254*l3 - 2.8976097455846508e-7, 2)*(3.3805884586533577e-11*pow(l1, 2) - 8.5799676844192251e-11*l1*l2 + 1.7734359124894555e-11*l1*l3 + 6.9660097893658595e-14*l1 + 5.4454499942327239e-11*pow(l2, 2) - 2.2533411313658251e-11*l2*l3 - 8.8360062021618894e-14*l2 + 2.3398679415951372e-12*pow(l3, 2) + 1.8233157487335451e-14*l3 + 3.5911606980184428e-17) - 1.0778171431223313e-20*pow(-0.53136729308729957*pow(l1, 2) + l1*l2 + 0.069303355150411347*l1*l3 - 0.0010044837049652093*l1 - 0.41322169326549862*pow(l2, 2) - 0.17955474240371952*l2*l3 + 0.00091530179173831324*l2 + 0.054820196689620862*pow(l3, 2) + 9.5336285464630731e-5*l3 - 4.7130927941571089e-7, 2)*(1.3896016144405879e-11*pow(l1, 2) + 1.1382643353824243e-11*l1*l2 - 3.928377357858052e-11*l1*l3 + 1.6885767684884951e-14*l1 + 2.3398679415951368e-12*pow(l2, 2) - 1.6107121864743881e-11*l2*l3 + 6.8977121693380292e-15*l2 + 2.7772582237026216e-11*pow(l3, 2) - 2.3849704171574322e-14*l3 + 5.1389001336921739e-18) + 2*(-5.5165475065185872e-11*pow(l1, 2) + 1.0381797258289777e-10*l1*l2 + 7.1949338249082319e-12*l1*l3 - 1.0428346174204566e-13*l1 - 4.2899838422096126e-11*pow(l2, 2) - 1.8641009323998624e-11*l2*l3 + 9.5024776319765406e-14*l2 + 5.6913216769121215e-12*pow(l3, 2) + 9.8976198705223475e-15*l3 - 4.8930373848445577e-17)*(-3.5367410853738339e-11*pow(l1, 2) + 7.1949338249082319e-12*l1*l2 + 6.3878703884596147e-11*l1*l3 - 5.1905837941352888e-14*l1 + 8.8671795624472777e-12*pow(l2, 2) - 2.4932305151384002e-11*l2*l3 + 7.5507477351706682e-16*l2 - 1.9641886789290257e-11*pow(l3, 2) + 5.1391426246660414e-14*l3 - 1.8509555491132188e-17)*(2.1671405104185884e-11*pow(l1, 2) - 1.8641009323998624e-11*l1*l2 - 2.4932305151384002e-11*l1*l3 + 3.5494223739988346e-14*l1 - 1.1266705656829124e-11*pow(l2, 2) + 4.1222747249460305e-11*l2*l3 - 7.5964125609303015e-15*l2 - 8.0535609323719406e-12*pow(l3, 2) - 2.8073636513462422e-14*l3 + 1.3584774706293312e-17) + (1.3896016144405879e-11*pow(l1, 2) + 1.1382643353824243e-11*l1*l2 - 3.928377357858052e-11*l1*l3 + 1.6885767684884951e-14*l1 + 2.3398679415951368e-12*pow(l2, 2) - 1.6107121864743881e-11*l2*l3 + 6.8977121693380292e-15*l2 + 2.7772582237026216e-11*pow(l3, 2) - 2.3849704171574322e-14*l3 + 5.1389001336921739e-18)*(3.3805884586533577e-11*pow(l1, 2) - 8.5799676844192251e-11*l1*l2 + 1.7734359124894555e-11*l1*l3 + 6.9660097893658595e-14*l1 + 5.4454499942327239e-11*pow(l2, 2) - 2.2533411313658251e-11*l2*l3 - 8.8360062021618894e-14*l2 + 2.3398679415951372e-12*pow(l3, 2) + 1.8233157487335451e-14*l3 + 3.5911606980184428e-17)*(9.0023941147560682e-11*pow(l1, 2) - 1.1033095013037174e-10*l1*l2 - 7.0734821707476691e-11*l1*l3 + 1.5485444573210494e-13*l1 + 3.3805884586533577e-11*pow(l2, 2) + 4.3342810208371768e-11*l2*l3 - 9.4911915884298407e-14*l2 + 1.3896016144405875e-11*pow(l3, 2) - 6.0817043275540881e-14*l3 + 6.6668760917630031e-17) - (9.0023941147560682e-11*pow(l1, 2) - 1.1033095013037174e-10*l1*l2 - 7.0734821707476691e-11*l1*l3 + 1.5485444573210494e-13*l1 + 3.3805884586533577e-11*pow(l2, 2) + 4.3342810208371768e-11*l2*l3 - 9.4911915884298407e-14*l2 + 1.3896016144405875e-11*pow(l3, 2) - 6.0817043275540881e-14*l3 + 6.6668760917630031e-17)*1.6993148907928871e-21*pow(0.52571472185104329*pow(l1, 2) - 0.4522020138830673*l1*l2 - 0.6048191063178211*l1*l3 + 0.00086103489234218961*l1 - 0.27331282868287315*pow(l2, 2) + l2*l3 - 0.00018427720294720908*l2 - 0.19536691437947235*pow(l3, 2) - 0.00068102293967877087*l3 + 3.2954559345801892e-7, 2)) + (-(-5.5165475065185872e-11*pow(l1, 2) + 1.0381797258289777e-10*l1*l2 + 7.1949338249082319e-12*l1*l3 - 1.0428346174204566e-13*l1 - 4.2899838422096126e-11*pow(l2, 2) - 1.8641009323998624e-11*l2*l3 + 9.5024776319765406e-14*l2 + 5.6913216769121215e-12*pow(l3, 2) + 9.8976198705223475e-15*l3 - 4.8930373848445577e-17)*(1.3896016144405879e-11*pow(l1, 2) + 1.1382643353824243e-11*l1*l2 - 3.928377357858052e-11*l1*l3 + 1.6885767684884951e-14*l1 + 2.3398679415951368e-12*pow(l2, 2) - 1.6107121864743881e-11*l2*l3 + 6.8977121693380292e-15*l2 + 2.7772582237026216e-11*pow(l3, 2) - 2.3849704171574322e-14*l3 + 5.1389001336921739e-18) + (-3.5367410853738339e-11*pow(l1, 2) + 7.1949338249082319e-12*l1*l2 + 6.3878703884596147e-11*l1*l3 - 5.1905837941352888e-14*l1 + 8.8671795624472777e-12*pow(l2, 2) - 2.4932305151384002e-11*l2*l3 + 7.5507477351706682e-16*l2 - 1.9641886789290257e-11*pow(l3, 2) + 5.1391426246660414e-14*l3 - 1.8509555491132188e-17)*(2.1671405104185884e-11*pow(l1, 2) - 1.8641009323998624e-11*l1*l2 - 2.4932305151384002e-11*l1*l3 + 3.5494223739988346e-14*l1 - 1.1266705656829124e-11*pow(l2, 2) + 4.1222747249460305e-11*l2*l3 - 7.5964125609303015e-15*l2 - 8.0535609323719406e-12*pow(l3, 2) - 2.8073636513462422e-14*l3 + 1.3584774706293312e-17))*(l1_dot*(3.5367410853738332e-11*l1 + 1.4476471279277652e-11*l2 - 4.9982687740190272e-11*l3 + 2.1497316303582448e-14) + l1_dot*(3.5367410853738339e-11*l1 - 2.1671405104185884e-11*l2 - 1.3896016144405875e-11*l3 + 3.040852163777044e-14) + l2_dot*(6.6704799256580735e-12*l1 - 1.2012827476139967e-11*l2 + 5.2904183620937451e-12*l3 + 7.5710638665775006e-15) - l2_dot*(2.1671405104185884e-11*l1 - 2.7508188886445901e-11*l2 + 5.6913216769121215e-12*l3 + 2.2318384418496813e-14) + l3_dot*(-1.3896016144405882e-11*l1 - 5.6913216769121215e-12*l2 + 1.9641886789290263e-11*l3 - 8.4428838424424756e-15) - l3_dot*(1.3896016144405882e-11*l1 + 5.6913216769121215e-12*l2 - 1.9641886789290263e-11*l3 + 8.4428838424424756e-15))/(-4.0804888099759188e-21*pow(-0.55366512942456425*pow(l1, 2) + 0.11263431139596485*l1*l2 + l1*l3 - 0.00081256874020372194*l1 + 0.13881276580794133*pow(l2, 2) - 0.39030699803219132*l2*l3 + 1.1820446057909876e-5*l2 - 0.30748724684169343*pow(l3, 2) + 0.00080451579511545254*l3 - 2.8976097455846508e-7, 2)*(3.3805884586533577e-11*pow(l1, 2) - 8.5799676844192251e-11*l1*l2 + 1.7734359124894555e-11*l1*l3 + 6.9660097893658595e-14*l1 + 5.4454499942327239e-11*pow(l2, 2) - 2.2533411313658251e-11*l2*l3 - 8.8360062021618894e-14*l2 + 2.3398679415951372e-12*pow(l3, 2) + 1.8233157487335451e-14*l3 + 3.5911606980184428e-17) - 1.0778171431223313e-20*pow(-0.53136729308729957*pow(l1, 2) + l1*l2 + 0.069303355150411347*l1*l3 - 0.0010044837049652093*l1 - 0.41322169326549862*pow(l2, 2) - 0.17955474240371952*l2*l3 + 0.00091530179173831324*l2 + 0.054820196689620862*pow(l3, 2) + 9.5336285464630731e-5*l3 - 4.7130927941571089e-7, 2)*(1.3896016144405879e-11*pow(l1, 2) + 1.1382643353824243e-11*l1*l2 - 3.928377357858052e-11*l1*l3 + 1.6885767684884951e-14*l1 + 2.3398679415951368e-12*pow(l2, 2) - 1.6107121864743881e-11*l2*l3 + 6.8977121693380292e-15*l2 + 2.7772582237026216e-11*pow(l3, 2) - 2.3849704171574322e-14*l3 + 5.1389001336921739e-18) + 2*(-5.5165475065185872e-11*pow(l1, 2) + 1.0381797258289777e-10*l1*l2 + 7.1949338249082319e-12*l1*l3 - 1.0428346174204566e-13*l1 - 4.2899838422096126e-11*pow(l2, 2) - 1.8641009323998624e-11*l2*l3 + 9.5024776319765406e-14*l2 + 5.6913216769121215e-12*pow(l3, 2) + 9.8976198705223475e-15*l3 - 4.8930373848445577e-17)*(-3.5367410853738339e-11*pow(l1, 2) + 7.1949338249082319e-12*l1*l2 + 6.3878703884596147e-11*l1*l3 - 5.1905837941352888e-14*l1 + 8.8671795624472777e-12*pow(l2, 2) - 2.4932305151384002e-11*l2*l3 + 7.5507477351706682e-16*l2 - 1.9641886789290257e-11*pow(l3, 2) + 5.1391426246660414e-14*l3 - 1.8509555491132188e-17)*(2.1671405104185884e-11*pow(l1, 2) - 1.8641009323998624e-11*l1*l2 - 2.4932305151384002e-11*l1*l3 + 3.5494223739988346e-14*l1 - 1.1266705656829124e-11*pow(l2, 2) + 4.1222747249460305e-11*l2*l3 - 7.5964125609303015e-15*l2 - 8.0535609323719406e-12*pow(l3, 2) - 2.8073636513462422e-14*l3 + 1.3584774706293312e-17) + (1.3896016144405879e-11*pow(l1, 2) + 1.1382643353824243e-11*l1*l2 - 3.928377357858052e-11*l1*l3 + 1.6885767684884951e-14*l1 + 2.3398679415951368e-12*pow(l2, 2) - 1.6107121864743881e-11*l2*l3 + 6.8977121693380292e-15*l2 + 2.7772582237026216e-11*pow(l3, 2) - 2.3849704171574322e-14*l3 + 5.1389001336921739e-18)*(3.3805884586533577e-11*pow(l1, 2) - 8.5799676844192251e-11*l1*l2 + 1.7734359124894555e-11*l1*l3 + 6.9660097893658595e-14*l1 + 5.4454499942327239e-11*pow(l2, 2) - 2.2533411313658251e-11*l2*l3 - 8.8360062021618894e-14*l2 + 2.3398679415951372e-12*pow(l3, 2) + 1.8233157487335451e-14*l3 + 3.5911606980184428e-17)*(9.0023941147560682e-11*pow(l1, 2) - 1.1033095013037174e-10*l1*l2 - 7.0734821707476691e-11*l1*l3 + 1.5485444573210494e-13*l1 + 3.3805884586533577e-11*pow(l2, 2) + 4.3342810208371768e-11*l2*l3 - 9.4911915884298407e-14*l2 + 1.3896016144405875e-11*pow(l3, 2) - 6.0817043275540881e-14*l3 + 6.6668760917630031e-17) - (9.0023941147560682e-11*pow(l1, 2) - 1.1033095013037174e-10*l1*l2 - 7.0734821707476691e-11*l1*l3 + 1.5485444573210494e-13*l1 + 3.3805884586533577e-11*pow(l2, 2) + 4.3342810208371768e-11*l2*l3 - 9.4911915884298407e-14*l2 + 1.3896016144405875e-11*pow(l3, 2) - 6.0817043275540881e-14*l3 + 6.6668760917630031e-17)*1.6993148907928871e-21*pow(0.52571472185104329*pow(l1, 2) - 0.4522020138830673*l1*l2 - 0.6048191063178211*l1*l3 + 0.00086103489234218961*l1 - 0.27331282868287315*pow(l2, 2) + l2*l3 - 0.00018427720294720908*l2 - 0.19536691437947235*pow(l3, 2) - 0.00068102293967877087*l3 + 3.2954559345801892e-7, 2)) + (-4.0804888099759188e-21*pow(-0.55366512942456425*pow(l1, 2) + 0.11263431139596485*l1*l2 + l1*l3 - 0.00081256874020372194*l1 + 0.13881276580794133*pow(l2, 2) - 0.39030699803219132*l2*l3 + 1.1820446057909876e-5*l2 - 0.30748724684169343*pow(l3, 2) + 0.00080451579511545254*l3 - 2.8976097455846508e-7, 2) + (1.3896016144405879e-11*pow(l1, 2) + 1.1382643353824243e-11*l1*l2 - 3.928377357858052e-11*l1*l3 + 1.6885767684884951e-14*l1 + 2.3398679415951368e-12*pow(l2, 2) - 1.6107121864743881e-11*l2*l3 + 6.8977121693380292e-15*l2 + 2.7772582237026216e-11*pow(l3, 2) - 2.3849704171574322e-14*l3 + 5.1389001336921739e-18)*(9.0023941147560682e-11*pow(l1, 2) - 1.1033095013037174e-10*l1*l2 - 7.0734821707476691e-11*l1*l3 + 1.5485444573210494e-13*l1 + 3.3805884586533577e-11*pow(l2, 2) + 4.3342810208371768e-11*l2*l3 - 9.4911915884298407e-14*l2 + 1.3896016144405875e-11*pow(l3, 2) - 6.0817043275540881e-14*l3 + 6.6668760917630031e-17))*(l1_dot*(-2.1671405104185884e-11*l1 - 8.8671795624472777e-12*l2 + 3.0623626828296123e-11*l3 - 1.3175839321491533e-14) - l1_dot*(1.3865413750566305e-11*l1 + 5.7215316487545886e-12*l2 - 1.9641886789290257e-11*l3 + 8.3261386400945674e-15) + l2_dot*(6.1748567483066227e-12*l1 + 4.3144784938388404e-11*l2 - 4.9276308181832249e-11*l3 - 6.4404056958009092e-15) + l2_dot*(1.2466152575691999e-11*l1 - 2.0611373624730153e-11*l2 + 8.0535609323719406e-12*l3 + 1.4036818256731211e-14) + 2*l3_dot*(1.4844125366861375e-12*l1 + 2.6325066615506958e-11*l2 - 2.7772582237026216e-11*l3 - 5.5608222556130647e-15))/(-4.0804888099759188e-21*pow(-0.55366512942456425*pow(l1, 2) + 0.11263431139596485*l1*l2 + l1*l3 - 0.00081256874020372194*l1 + 0.13881276580794133*pow(l2, 2) - 0.39030699803219132*l2*l3 + 1.1820446057909876e-5*l2 - 0.30748724684169343*pow(l3, 2) + 0.00080451579511545254*l3 - 2.8976097455846508e-7, 2)*(3.3805884586533577e-11*pow(l1, 2) - 8.5799676844192251e-11*l1*l2 + 1.7734359124894555e-11*l1*l3 + 6.9660097893658595e-14*l1 + 5.4454499942327239e-11*pow(l2, 2) - 2.2533411313658251e-11*l2*l3 - 8.8360062021618894e-14*l2 + 2.3398679415951372e-12*pow(l3, 2) + 1.8233157487335451e-14*l3 + 3.5911606980184428e-17) - 1.0778171431223313e-20*pow(-0.53136729308729957*pow(l1, 2) + l1*l2 + 0.069303355150411347*l1*l3 - 0.0010044837049652093*l1 - 0.41322169326549862*pow(l2, 2) - 0.17955474240371952*l2*l3 + 0.00091530179173831324*l2 + 0.054820196689620862*pow(l3, 2) + 9.5336285464630731e-5*l3 - 4.7130927941571089e-7, 2)*(1.3896016144405879e-11*pow(l1, 2) + 1.1382643353824243e-11*l1*l2 - 3.928377357858052e-11*l1*l3 + 1.6885767684884951e-14*l1 + 2.3398679415951368e-12*pow(l2, 2) - 1.6107121864743881e-11*l2*l3 + 6.8977121693380292e-15*l2 + 2.7772582237026216e-11*pow(l3, 2) - 2.3849704171574322e-14*l3 + 5.1389001336921739e-18) + 2*(-5.5165475065185872e-11*pow(l1, 2) + 1.0381797258289777e-10*l1*l2 + 7.1949338249082319e-12*l1*l3 - 1.0428346174204566e-13*l1 - 4.2899838422096126e-11*pow(l2, 2) - 1.8641009323998624e-11*l2*l3 + 9.5024776319765406e-14*l2 + 5.6913216769121215e-12*pow(l3, 2) + 9.8976198705223475e-15*l3 - 4.8930373848445577e-17)*(-3.5367410853738339e-11*pow(l1, 2) + 7.1949338249082319e-12*l1*l2 + 6.3878703884596147e-11*l1*l3 - 5.1905837941352888e-14*l1 + 8.8671795624472777e-12*pow(l2, 2) - 2.4932305151384002e-11*l2*l3 + 7.5507477351706682e-16*l2 - 1.9641886789290257e-11*pow(l3, 2) + 5.1391426246660414e-14*l3 - 1.8509555491132188e-17)*(2.1671405104185884e-11*pow(l1, 2) - 1.8641009323998624e-11*l1*l2 - 2.4932305151384002e-11*l1*l3 + 3.5494223739988346e-14*l1 - 1.1266705656829124e-11*pow(l2, 2) + 4.1222747249460305e-11*l2*l3 - 7.5964125609303015e-15*l2 - 8.0535609323719406e-12*pow(l3, 2) - 2.8073636513462422e-14*l3 + 1.3584774706293312e-17) + (1.3896016144405879e-11*pow(l1, 2) + 1.1382643353824243e-11*l1*l2 - 3.928377357858052e-11*l1*l3 + 1.6885767684884951e-14*l1 + 2.3398679415951368e-12*pow(l2, 2) - 1.6107121864743881e-11*l2*l3 + 6.8977121693380292e-15*l2 + 2.7772582237026216e-11*pow(l3, 2) - 2.3849704171574322e-14*l3 + 5.1389001336921739e-18)*(3.3805884586533577e-11*pow(l1, 2) - 8.5799676844192251e-11*l1*l2 + 1.7734359124894555e-11*l1*l3 + 6.9660097893658595e-14*l1 + 5.4454499942327239e-11*pow(l2, 2) - 2.2533411313658251e-11*l2*l3 - 8.8360062021618894e-14*l2 + 2.3398679415951372e-12*pow(l3, 2) + 1.8233157487335451e-14*l3 + 3.5911606980184428e-17)*(9.0023941147560682e-11*pow(l1, 2) - 1.1033095013037174e-10*l1*l2 - 7.0734821707476691e-11*l1*l3 + 1.5485444573210494e-13*l1 + 3.3805884586533577e-11*pow(l2, 2) + 4.3342810208371768e-11*l2*l3 - 9.4911915884298407e-14*l2 + 1.3896016144405875e-11*pow(l3, 2) - 6.0817043275540881e-14*l3 + 6.6668760917630031e-17) - (9.0023941147560682e-11*pow(l1, 2) - 1.1033095013037174e-10*l1*l2 - 7.0734821707476691e-11*l1*l3 + 1.5485444573210494e-13*l1 + 3.3805884586533577e-11*pow(l2, 2) + 4.3342810208371768e-11*l2*l3 - 9.4911915884298407e-14*l2 + 1.3896016144405875e-11*pow(l3, 2) - 6.0817043275540881e-14*l3 + 6.6668760917630031e-17)*1.6993148907928871e-21*pow(0.52571472185104329*pow(l1, 2) - 0.4522020138830673*l1*l2 - 0.6048191063178211*l1*l3 + 0.00086103489234218961*l1 - 0.27331282868287315*pow(l2, 2) + l2*l3 - 0.00018427720294720908*l2 - 0.19536691437947235*pow(l3, 2) - 0.00068102293967877087*l3 + 3.2954559345801892e-7, 2));
   return A_4_5_result;

}
