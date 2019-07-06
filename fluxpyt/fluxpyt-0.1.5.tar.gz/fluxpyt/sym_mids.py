def sym_mids(stoich_matrix, model_metabolite, rxnId_networks, rxn_networks,
             measured_mids, substrate_mids, rates):
    """
    prints the calculated mids. Written so as to be helpful in making MFA model
    """
    from fluxpyt.free_flux_null import get_null_mat
    import sympy as sp
    import random
    from fluxpyt.solve_mid_networks import solve_mid_networks

    # cal_mids = solve_mid_networks(rxnId_networks_g, rxn_networks_g,
    #                              substrate_mids_g, rates_g, flux_dist_g)

    print('Here we go')

    # free flux through nullspace()
    [null_mat, free_ind] = get_null_mat(stoich_matrix, model_metabolite)
    rxn_ids = model_metabolite[0]
    free_ind = [x for x in free_ind]
    free_ids = [rxn_ids[x] for x in free_ind]
    p_basis = model_metabolite[6][0]

    free_fluxes = []
    for id in free_ids:
        free_fluxes.append(random.random() * p_basis * 3)

    free_fluxes = sp.Matrix(free_fluxes)
    sol = null_mat * free_fluxes
    fluxes = [z for z in sol]
    flux_dist = [rxn_ids, fluxes]

    print('\n\n',substrate_mids)

    cal_mids = solve_mid_networks(rxnId_networks, rxn_networks,
                                  substrate_mids, rates, flux_dist)
    print('\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n',len(rxn_networks))

    print('\n\n',rates)
    print('\n\n',flux_dist)
    print('\n\n')

    print('\ncal_mids:\n',cal_mids,'\n\n')
    print('\n\n', measured_mids[2], '\n\n', cal_mids[0])

    print('\n\nFollowing measured mids can be simulated:\n')
    for emu in measured_mids[2]:
        if emu in cal_mids[0]:
            print(emu, '\tTrue')
        else:
            print(emu, '\tFalse')

    return None
