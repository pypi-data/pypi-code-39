import libsbml
from . import utils
import argparse
from contextlib import redirect_stdout


def run():
    #Files are given in argument on the same line than the execution line 
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('regulatory', type=str,
                        help='regulatory network')
    parser.add_argument('caspo', type=str,
                        help='caspo out')
    args = parser.parse_args()

    network_regu = args.regulatory
    caspo_out = args.caspo
    #Parsing regulation file
    reader_regu = libsbml.SBMLReader()
    document_regu = reader_regu.readSBML(network_regu)
    document_regu.setPackageRequired('qual', True)
    model_regu = document_regu.getModel()
    mplugin = model_regu.getPlugin("qual")

    # collect the lists to parse or use after
    listCompartments = model_regu.getListOfCompartments()
    listSpecies_regu = mplugin.getListOfQualitativeSpecies()
    listTransitions = mplugin.getListOfTransitions()

    # take the result form caspo and keep only the ones that are important (at 1)
    caspo = utils.parse_caspo(caspo_out)
    nb_network = len(caspo[1])
    ''' We keep the id for transitions already exist to see if we can get it directly
        rather than create new ones by default ''' 
    d_T = {}
    d_T = utils.r_get_transitions(listTransitions)
    id_tr = []
    for k in d_T.keys():
        id_tr.append(k.replace('tr_', ''))
    ''' We create a new regulatory network for each lines contained in the caspo file
        (Each line represent a possible regulation)''' 
    for i in range(nb_network):
        sbmlns = libsbml.SBMLNamespaces(3, 1,'qual', 1)
        document = libsbml.SBMLDocument(sbmlns)
        document.setPackageRequired('qual', True)
        model=document.createModel()
        name=model_regu.getName()
        model.setName(name)
        id_model=model_regu.getId()
        model.setId(id_model)
        mplugin = model.getPlugin("qual")
        list_to_add = caspo[1][i]
        species_regu = utils.r_get_species(listSpecies_regu)
        transitions = utils.r_get_transitions(listTransitions)
        comp = utils.r_get_compart(listCompartments)
        utils.r_set_compart(model, comp)
        for k in comp.keys():
            comp_default=k

        allp = set()
        for elem in list_to_add:
            elem = elem.split('<-')
            e_input = elem[1]
            e_output = elem[0]

            if '+' in e_input:
                e_input = list(e_input.split('+'))
            else: e_input = [e_input]
           
            if '+' in e_output:
                e_output = list(e_output.split('+'))
            else: e_output = [e_output]
            #Creation of list with the species who as exclamation mark 
            newinput = []
            inputpoint = []
            for elt in e_input:
                if '!' in elt:
                    newinput.append(elt.replace('!', ''))
                    inputpoint.append(elt.replace('!', ''))
                else:
                    newinput.append(elt.replace('!', ''))

            e_input = list(newinput)
            #Creation of the set used for intizialise the species (set allow unique species)
            [allp.add(element) for element in e_input]
            [allp.add(element) for element in e_output]


            ''' We first create all the list and set to collect the information 
            We begin with the real creation of regulation reaction (call transitions here)
            Then we will initialize all the species, need to determine if we need them all 
            or just the one which are  implies in the transitions present'''
            # if e_output[0] in id_tr :
            #     utils.r_set_transitions(model, mplugin, transitions, e_input, inputpoint, e_output, str('tr_'+e_output[0]))
            # else:
            #     utils.r_set_transitions_default(model, mplugin, e_input, inputpoint, e_output, str('tr_'+e_output[0]))

            utils.r_set_transitions_default(model, mplugin, e_input, inputpoint, e_output, str('tr_'+e_output[0]))

        for name in allp:
            if name in species_regu.keys(): 
                utils.r_set_species(model, mplugin, species_regu, name)
            else:
                utils.r_set_species_default(model, mplugin, name, comp_default)
        #Print in output the new regulatory networks :
        nb=str(i)
        network_regu_name=str('network_regulatory_'+nb+'.xml')
        regu=libsbml.writeSBMLToString(document)            
        with open(network_regu_name, 'w') as f:
             with redirect_stdout(f):
                 print(regu)

if __name__ == '__main__':
    run()
