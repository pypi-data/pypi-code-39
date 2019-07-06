import sys
from copy import deepcopy

def check_model(filename):
    """

    """

    import fluxpyt.build_model as bm
    import time
    import fluxpyt.create_atm_transition_equations as cae
    import fluxpyt.priliminary_fba as pf
    import fluxpyt.solve_mid_networks as smn
    import fluxpyt.input_substrate_emu as ise
    from copy import deepcopy
    from fluxpyt.solve_mfa_lm import solve_mfa_problem
    from fluxpyt.utility import space
    from fluxpyt.make_emu_networks import make_networks as mn2

    t1 = time.time()

    # build model
    filepath = filename + '.csv'

    [stoich_matrix, model_metabolite, model_isotope,
     mets, mids] = bm.build_model(filepath)

    end_nodes(stoich_matrix,mets)
    
#    print('\n\n*********************')
#    
#    for i,rxn in enumerate(model_metabolite[1]):
#        if rxn == 'ASP + PYR + GLU + SucCoA + ATP + 2 NADPH -> 0.5 LYS + 0.5 LYS + 0.5 CO2 + 0.5 CO2 + AKG + SUC':
#            pep_ind = mets.index('CO2')
#            print(stoich_matrix[pep_ind][i])
#        
#    
#    maximize_rxn('R95',model_metabolite, stoich_matrix)
    
    sys.exit()

def maximize_rxn(rxnId,model_metabolite, stoich_matrix):
    '''
    Checks model feasibility. Returns flux variability and initial solution.
    '''
    
    from fluxpyt.priliminary_fba import create_objective, sort_glpk_solution, flux_range
    from fluxpyt.glpk_solve import glpk_solve
    
    rxnInd = model_metabolite[0].index(rxnId)
    [mat,c,b,bounds] = create_objective(stoich_matrix,model_metabolite,rxnInd,maximize=False)
    c_min = deepcopy(c)
    c_max = [x*-1 for x in c_min]
#    minFlux =  glpk_solve(mat, c, b, bounds, model_metabolite[0], maximize=False)
#    assert minFlux.status == 'OPTIMAL', 'No feasible solution found for the basis provided.'

    maxFlux =  glpk_solve(mat, c, b, bounds, model_metabolite[0], maximize=True)
    assert maxFlux.status == 'OPTIMAL', 'No feasible solution found for the basis provided.'
    
    print('\n\n', dir(maxFlux),'\n\n', maxFlux.x,'\n\n',model_metabolite[0])
    print('\n\n*********************')
    
    file = open('fluxDist.csv','w')
    for i,r in enumerate(maxFlux.x[0]):
        ind = model_metabolite[0].index(r)
        print('\n',model_metabolite[0][ind],r,maxFlux.x[1][i],model_metabolite[1][ind])
        file.write(str(model_metabolite[0][ind]) + ',' + r + ',' + str(maxFlux.x[1][i]) + ',' + model_metabolite[1][ind] + '\n')
    file.close()

def end_nodes(stoich_matrix,metList):
    """ 
    Detect dead-end metabolites.
    """
    end_mets = []
    for i, rows in enumerate(stoich_matrix):
        g0 = len([x for x in rows if x > 0])
        l0 = len([x for x in rows if x < 0])
        #print(metList[i],l0,g0)
        if l0 > 0 and g0 == 0:
            end_mets.append(metList[i])
        elif l0 == 0 and g0 > 0:
            end_mets.append(metList[i])
    print('\n\n',metList,'\n\n')
    print('\nend_mets\n',end_mets)
    
    return end_mets