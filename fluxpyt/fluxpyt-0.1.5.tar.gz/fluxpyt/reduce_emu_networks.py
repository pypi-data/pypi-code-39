# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 13:22:20 2016

@author: Trunil
"""
#from utility import space
#from utility import split_rxn
#import solve_mid_networks as smn
#from copy import deepcopy
#import sys
from fluxpyt.build_model import make_stoich_matrix
#from fluxpyt.build_model import metabolite_list
#from utility import size
#import numpy as np
                
                
def reduce_emu_networks(rxnId_networks,rxn_networks):
    
    
    for i, network in enumerate(rxn_networks):
        print('\n\nNetwork:\n',rxn_networks)
        rxn_id_net = rxnId_networks[i]
        
        mets = metabolite_list(network)
        stoich_matrix = make_stoich_matrix(rxn_id_net, network)
        
        print('\n\n',mets, '\n\n', rxn_id_net,'\n\n', size(stoich_matrix))
        
        
        loopTag = True
        while loopTag:
            new_S = []
            # find row with one positive value and indice of the positive value
            for stoich_count,row1 in enumerate(stoich_matrix):
                print('*'*10)
                print('\nrow1',row1)
                num_pos = len([x for x in row1 if x>0]) # forming
                if num_pos == 1:
                    c1 = [x for x,i in enumerate(row1) if i>0][0] #column which has the positive value
                
                    r2s = []
                    for r2ind, row2 in enumerate(stoich_matrix):
                        print('\nrow2',row2)
                        if row2[c1] < 0:
                            r2s.append(r2ind)
                    if len(r2s) == 1: # if only one negative value in the reaction
                        print('r2s',r2s)
                        R2 = stoich_matrix[r2s]
                        print('R2: ',R2[0])
                        R1Sr2c1 = [x*R2[0][c1]/row1[c1] for x in row1]
                        R2 = np.array([x+y for x,y in zip(R1Sr2c1,R2[0])])
                        print('\nR2',R2)
                        stoich_matrix = np.append(stoich_matrix,R2)
                
               
                    
            loopTag = False
                    
                    
                    
        #print(size(new_S))
        
        return 3,4
    
                



        
        
#       
#n = [['1 A -> 2 B','1 C -> 1 B','1 B -> 1 B1','1 B1 -> 1 D','1 D -> 1 E','1 D -> 1 F','F -> B'],['1 A -> 1 B','1 C -> 1 B','1 B -> 1 B1','1 B1 -> 1 D','1 D -> 1 E','1 D -> 1 F']]
#
#v = [['V1','V2','V3','V4','V5','V6','V7'],['V1','V2','V3','V4','V5','V6']]
##[a,b,c] = mol_red(v[0],n[0])
#[a,b] = reduce_emu_networks(v,n)


        
        
        
        