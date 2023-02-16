\ Model VoT
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  1.025 x_eu[0,0] + 2.05 x_eu[0,1] + 0.5857142857142856 x_eu[1,0]
   + 1.171428571428571 x_eu[1,1] + 0.5857142857142856 x_eu[2,0]
   + 1.171428571428571 x_eu[2,1] + 0.6833333333333332 x_eu[3,0]
   + 1.366666666666666 x_eu[3,1] + 0.6833333333333332 x_eu[4,0]
   + 1.366666666666666 x_eu[4,1] + 1.025 x_eu[5,0] + 2.05 x_eu[5,1]
   + 1.025 x_eu[6,0] + 2.05 x_eu[6,1] + [ 2.4 x_eu[0,0] * eps[0]
   + 4.8 x_eu[0,1] * eps[0] + 2.4 x_eu[1,0] * eps[1]
   + 4.8 x_eu[1,1] * eps[1] + 2.4 x_eu[2,0] * eps[2]
   + 4.8 x_eu[2,1] * eps[2] + 2.4 x_eu[3,0] * eps[3]
   + 4.8 x_eu[3,1] * eps[3] + 2.4 x_eu[4,0] * eps[4]
   + 4.8 x_eu[4,1] * eps[4] + 2.4 x_eu[5,0] * eps[5]
   + 4.8 x_eu[5,1] * eps[5] + 2.4 x_eu[6,0] * eps[6]
   + 4.8 x_eu[6,1] * eps[6] ] / 2 
Subject To
 R0: x_eu[0,0] + x_eu[0,1] - x_e[0] = 0
 R1: x_eu[1,0] + x_eu[1,1] - x_e[1] = 0
 R2: x_eu[2,0] + x_eu[2,1] - x_e[2] = 0
 R3: x_eu[3,0] + x_eu[3,1] - x_e[3] = 0
 R4: x_eu[4,0] + x_eu[4,1] - x_e[4] = 0
 R5: x_eu[5,0] + x_eu[5,1] - x_e[5] = 0
 R6: x_eu[6,0] + x_eu[6,1] - x_e[6] = 0
 R7: x_eu[0,0] + x_eu[1,0] + x_eu[3,0] + x_eu[5,0] = 10
 R8: x_eu[0,1] + x_eu[1,1] + x_eu[3,1] + x_eu[5,1] = 10
 R9: <= 0
 R10: <= 0
 R11: x_eu[0,0] + x_eu[2,0] + x_eu[4,0] + x_eu[6,0] = 10
 R12: x_eu[0,1] + x_eu[2,1] + x_eu[4,1] + x_eu[6,1] = 10
 R13: <= 0
 R14: <= 0
 R15: x_eu[1,0] - x_eu[2,0] = 0
 R16: x_eu[3,0] - x_eu[4,0] = 0
 R17: x_eu[5,0] - x_eu[6,0] = 0
 R18: x_eu[1,1] - x_eu[2,1] = 0
 R19: x_eu[3,1] - x_eu[4,1] = 0
 R20: x_eu[5,1] - x_eu[6,1] = 0
 eps_edge0: eps[0] - x_e[0] >= -1.1
 eps_edge1: eps[1] - x_e[1] >= -2.2
 eps_edge2: eps[2] - x_e[2] >= -2.2
 eps_edge3: eps[3] - x_e[3] >= -4.4
 eps_edge4: eps[4] - x_e[4] >= -4.4
 eps_edge5: eps[5] - x_e[5] >= -6.6
 eps_edge6: eps[6] - x_e[6] >= -6.6
Bounds
End
