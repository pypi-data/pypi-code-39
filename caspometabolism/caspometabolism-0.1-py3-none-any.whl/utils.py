#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import libsbml


#Find the differents parameters from regulatory network in sbml
#Stored them to reuse after
def r_get_compart(listCompartments):
    d_Compartments={}                                       #All parameters are stored in dictionaries
    for i in listCompartments :
        d_Compartments[i.getId()]={    "name" :i.getName(),
                                    "constant":i.getConstant(),
                                }
    return d_Compartments

def r_get_species(listSpecies):
    d_Species_read={}
    for i in listSpecies :
        d_Species_read[i.getId()]={    "name" : i.getName(), 
                                "compartment" : i.getCompartment(),
                                "constant" : i.getConstant(),
                                "sboTerm": i.getSBOTerm(),
                                "initial" : i.getInitialLevel(),
                                "maxlevel" : i.getMaxLevel(),
                                "notes" : i.getNotes()                                
                            }
    return d_Species_read


def r_get_transitions(listTransitions):
    d_Transitions_read={}
    for i in listTransitions :
        #print ([i.getFunctionTerm(0).getMath()])
        d_Transitions_read[i.getId()]={    "inp" : [
                                            [inp.getSBOTerm() for inp in i.getListOfInputs()], 
                                            [inp.getId() for inp in i.getListOfInputs()],
                                            [inp.getQualitativeSpecies() for inp in i.getListOfInputs()],
                                            [inp.getTransitionEffect() for inp in i.getListOfInputs()],
                                            [inp.getSign() for inp in i.getListOfInputs()],
                                            ],
                                    "out" : [
                                            [out.getId() for out in i.getListOfOutputs()],
                                            [out.getQualitativeSpecies() for out in i.getListOfOutputs()],
                                            [out.getTransitionEffect() for out in i.getListOfOutputs()],
                                            ],
                                    "function":[
                                            [i.getFunctionTerm(0).getMath()],
                                            [i.getFunctionTerm(0).getResultLevel()]
                                            ],
                                    "default":[
                                            [i.getListOfFunctionTerms().getDefaultTerm().getResultLevel()],
                                    ]
                            }
        
    return d_Transitions_read
#Using the output of the Caspots identify 
#by put all the variable at 1 in a dico with key number of the line corresponding to.
def parse_caspo(caspo_file):
    with open(caspo_file, 'r') as f:
        header = f.readline()
        header = header.rstrip().split(',')
        dict_col = {}
        nb_col = len(header)
        cnt_line = 0
        
        for z in range(nb_col):
             dict_col[z] = []
        for line in f:
            line = line.rstrip()
            line = line.split(',')
            for z in range(nb_col):
                dict_col[z].append(int(line[z]))
            cnt_line += 1

    dico_h = {}
    for x, y in enumerate(header):
        dico_h[x] = y
        dico_h[y] = x
    
    spe = {}
    for i in range(cnt_line):
        spe[i] = []
    commun = []
    for k, v in dict_col.items():
        if sum(v) == int(cnt_line):
            commun.append(dico_h[k])
        else:
            for z in range(len(v)):
                if v[z] == 1:
                    spe[z].append(dico_h[k])
             
    return (commun, spe)

def r_set_compart(model, d_Compartments):
    for k, v in d_Compartments.items():
            c= model.createCompartment()
            c.setId(k)
            c.setName(v['name'])
            c.setConstant(v['constant'])
        
def r_set_species(model, mplugin, d_species, name):
    spe= mplugin.createQualitativeSpecies()
    spe.setId(name)
    spe.setName(d_species[name]['name'])
    spe.setCompartment(d_species[name]['compartment'])
    spe.setConstant(d_species[name]['constant'])
    spe.setInitialLevel(d_species[name]['initial'])
    spe.setMaxLevel(d_species[name]['maxlevel'])
    spe.setNotes(d_species[name]['notes'])    

#If the species is not in the regulatory file we create it by default

def r_set_species_default(model, mplugin, name, comp):
    spe= mplugin.createQualitativeSpecies()
    spe.setId(name)
    spe.setName(name)
    spe.setCompartment(comp)
    spe.setConstant(True)
    spe.setInitialLevel(1)
    spe.setMaxLevel(1)
    spe.setNotes('')

# def r_set_transitions (model, mplugin, d_Transitions, l_input,l_inputpoint, l_output, idx):
#     for k, v in d_Transitions.items():
#         if k == idx:
#             trans=mplugin.createTransition()
#             trans.setId(k)
#             for elem in l_input:
#                 inp=trans.createInput()
#                 for i in range (len (v['inp'][0])) :    
#                     name_species_input=str(inp.getQualitativeSpecies(elem))
#                     name_old_species_input=str(inp.getQualitativeSpecies(v['inp'][2][i]))
#                     print (name_species_input); print ( name_old_species_input)
#                     if name_old_species_input == name_species_input :
#                         inp.setSBOTerm(v['inp'][0][i])
#                         inp.setId((v['inp'][1][i]))                             
#                         inp.setQualitativeSpecies(v['inp'][2][i])
#                         inp.setTransitionEffect(v['inp'][3][i])
#                         inp.setSign(v['inp'][4][i])
#                     else :
#                         inp.setSBOTerm(1)                                           #Set SBOTerm by default 
#                         inp.setId(str('tr_'+elem+'_in_'+l_output[0]))               #Set the right fromat for ID corresponding to FlexFlux 
#                         inp.setQualitativeSpecies(elem)                             #elem correspond to the id of the input 
#                         inp.setTransitionEffect(libsbml.INPUT_TRANSITION_EFFECT_NONE)
#                         inp.setSign(libsbml.INPUT_SIGN_POSITIVE)


#             for elem in l_output:
#                 out=trans.createOutput()
#                 for j in range (len(v['out'][0])) :    
#                     name_species_output=out.setQualitativeSpecies(elem)
#                     name_old_species_output=out.setQualitativeSpecies(v['inp'][2][i]) 
#                     if name_old_species_output == name_species_output :
#                         out.setId(v['out'][0][j])
#                         out.setQualitativeSpecies(v['out'][1][j])
#                         out.setTransitionEffect(v['out'][2][j])
#                     else :
#                         out.setId(str('tr_'+elem+'_out'))
#                         out.setQualitativeSpecies(elem)
#                         out.setTransitionEffect(libsbml.INPUT_TRANSITION_EFFECT_NONE)
#             for elem in l_input:
#                 dt=trans.createDefaultTerm()
#                 if v['default'][0] :
#                     for n in range (len(v['default'][0])) :
#                                 dt.setResultLevel(v['default'][0][n])


#             fct=trans.createFunctionTerm()
#             fct.setResultLevel(1)

#             d_Math={}   #Creation of a dictionnary with the right values for each input 
#             if (len(l_input))>=2:
#                 for elem in l_input:
#                     if elem in l_inputpoint:
#                         for i in range (len(l_inputpoint)): 
#                            # math=libsbml.parseL3Formula(f'and (eq({l_inputpoint[i]}, 0), (eq({l_inputpoint[i+1]}),0)) ')
#                            d_Math[l_inputpoint[i]]=0
#                     else:
#                         for i in range (len(l_input)): 

#                             d_Math[l_input[i]]=1
#             else :
#                 if l_inputpoint:
#                     for i in range (len(l_inputpoint)): 
#                         d_Math[l_inputpoint[i]]=0

#                 else:
#                     for i in range (len(l_input)): 
#                         d_Math[l_input[i]]=1

#             #Creation of the mathematical function with <apply>
#             #concatenation of the string to give at libsbmlL3Fomula : 
#             eq_formul = ','.join([f'eq({k},{v})' for k, v in d_Math.items()])
#             if eq_formul.count('eq') >1 : 
#                 math = f'and({eq_formul})'
#             else:
#                 math = eq_formul
#             #Creation of the formule with L3Fomula
#             math = libsbml.parseL3Formula(math)
#             fct.setMath(math)


def r_set_transitions_default(model, mplugin, l_input, l_inputpoint, l_output, idx):
    trans=mplugin.createTransition()
    trans.setId(idx)

    for elem in l_input:
        inp=trans.createInput()#;print (elem)
        inp.setSBOTerm(1)                                           #Set SBOTerm by default 
        inp.setId(str('tr_'+elem+'_in_'+l_output[0]))               #Set the right fromat for ID corresponding to FlexFlux 
        inp.setQualitativeSpecies(elem)                             #elem correspond to the id of the input 
        inp.setTransitionEffect(libsbml.INPUT_TRANSITION_EFFECT_NONE)
        inp.setSign(libsbml.INPUT_SIGN_POSITIVE)

    
    for elem in l_output:
        out=trans.createOutput()
        out.setId(str('tr_'+elem+'_out'))
        out.setQualitativeSpecies(elem)
        out.setTransitionEffect(libsbml.INPUT_TRANSITION_EFFECT_NONE)


    fct=trans.createFunctionTerm()
    fct.setResultLevel(1)

    d_Math={}   #Creation of a dictionnary with the right values for the input 
    if (len(l_input))>=2:
        for elem in l_input:
            if elem in l_inputpoint:
                for i in range (len(l_inputpoint)): 
                   # math=libsbml.parseL3Formula(f'and (eq({l_inputpoint[i]}, 0), (eq({l_inputpoint[i+1]}),0)) ')
                   d_Math[l_inputpoint[i]]=0
            else:
                for i in range (len(l_input)): 

                    d_Math[l_input[i]]=1
    else :
        if l_inputpoint:
            for i in range (len(l_inputpoint)): 
                d_Math[l_inputpoint[i]]=0

        else:
            for i in range (len(l_input)): 
                d_Math[l_input[i]]=1

    #Creation of the mathematical function with <apply>
    #concatenation of the string to give at libsbmlL3Fomula : 
    eq_formul = ','.join([f'eq({k},{v})' for k, v in d_Math.items()])
    if eq_formul.count('eq') >1 : 
        math = f'and({eq_formul})'
    else:
        math = eq_formul
    #Creation of the formule with L3Fomula
    math = libsbml.parseL3Formula(math)
    fct.setMath(math)
     #Set of the default term for transition 
    dt=trans.createDefaultTerm()
    dt.setResultLevel(0)

