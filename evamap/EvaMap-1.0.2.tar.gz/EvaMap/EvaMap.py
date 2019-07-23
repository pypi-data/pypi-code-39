import rdflib
import yaml
import re
from rdflib.graph import Graph
import json

from EvaMap.Dimensions.Availability import Availability
from EvaMap.Dimensions.Clarity import Clarity
from EvaMap.Dimensions.Conciseness import Conciseness
from EvaMap.Dimensions.Connectability import Connectability
from EvaMap.Dimensions.Consistency import Consistency
from EvaMap.Dimensions.Coverability import Coverability


class EvaMap:

    g_link = Graph()
    g_map = Graph()
    g_onto = Graph()
    liste_map = []
    dimensions_list = [(Availability(), 1), (Clarity(), 1), (Conciseness(), 1), (Connectability(), 1), (Consistency(), 1), (Coverability(), 1)]
    score_tot = []
    final_list = []
    raw_data = {}
    final_score = 0

    def __init__(self, rdf_ontology, yarrrml_mapping, json_data):
        self.read_json(json_data)
        self.read_yaml(yarrrml_mapping)
        self.read_rdf(rdf_ontology)
        nbTriples = 0
        for triple in self.liste_map:
            nbTriples = nbTriples + 1
            self.g_link.add(triple)
            self.g_map.add(triple)
        weight = dict()

    def read_json(self, json_data):
        self.raw_data = json.loads(json_data)
        self.raw_data = self.raw_data["records"]

    def read_yaml(self, yarrrml_mapping):
        mapping = yaml.safe_load(yarrrml_mapping)
        self.liste_map = self.yamlToTriples(mapping)

    def yamlToTriples(self, mapping):
        liste_map = []
        prefString = ""
        for name in mapping["mappings"]:
            for predicateobject in mapping["mappings"][name]["predicateobjects"]:
                # on transforme les préfixes, si il y en a. Sinon on passe
                try:
                    for prefix in mapping["prefixes"]:
                        prefString = str(prefix) + ':'
                        if re.search(prefString, predicateobject[1]) is not None:
                            predicateobject[1] = mapping["prefixes"][prefix] + (
                                predicateobject[1].split(prefString, 1)[1])
                        if re.search(prefString, predicateobject[0]) is not None:
                            predicateobject[0] = mapping["prefixes"][prefix] + (
                                predicateobject[0].split(prefString, 1)[1])
                except:
                    pass
                # On regarde si c'est un littéral ou une URI
                if len(predicateobject) == 2:
                    if re.search('(http://)|(https://)', predicateobject[1]) is not None:
                        liste_map.append([rdflib.term.URIRef(mapping["mappings"][name]["subject"]),
                                          rdflib.term.URIRef(predicateobject[0]),
                                          rdflib.term.URIRef(predicateobject[1])])
                    else:
                        liste_map.append([rdflib.term.URIRef(mapping["mappings"][name]["subject"]),
                                          rdflib.term.URIRef(predicateobject[0]),
                                          rdflib.term.Literal(predicateobject[1])])

                # taille de 3 = littéral
                elif len(predicateobject) == 3:
                    if len(predicateobject[2].split('~')) == 2:
                        if predicateobject[2].split('~')[1] == 'lang':
                            liste_map.append([rdflib.term.URIRef(mapping["mappings"][name]["subject"]),
                                              rdflib.term.URIRef(predicateobject[0]),
                                              rdflib.term.Literal(predicateobject[1],
                                                                  lang=predicateobject[2].split('~')[0])])
                        else:
                            liste_map.append([rdflib.term.URIRef(mapping["mappings"][name]["subject"]),
                                              rdflib.term.URIRef(predicateobject[0]),
                                              rdflib.term.Literal(predicateobject[1], datatype=predicateobject[2])])
                    else:
                        liste_map.append([rdflib.term.URIRef(mapping["mappings"][name]["subject"]),
                                          rdflib.term.URIRef(predicateobject[0]),
                                          rdflib.term.Literal(predicateobject[1], datatype=predicateobject[2])])
        # on relie les variables aux mappings correspondant, jusque là considérées comme des litérals
        for name in mapping["mappings"]:
            for triples in liste_map:
                if str(triples[2]) == name:
                    triples[2] = rdflib.term.URIRef(mapping["mappings"][name]["subject"])
        return liste_map

    def read_rdf(self, rdf):
        for format in 'xml', 'turtle', 'nt':
            try:
                self.g_onto.parse(data=rdf, format=format)
                break
            except Exception:
                pass
        for s, p, o in self.g_onto.triples((None, None, None)):
            self.g_link.add((s, p, o))

    def set_weight(self, dict):
        i = 0
        for poids in self.liste :
            self.weight[i] = poids

    def evaluate_mapping(self):
        self.final_score = 0
        tot_weight = 0
        for dimension in self.dimensions_list:
            dimension_score = dimension[0].calc_score(self.g_onto, self.liste_map, self.g_map, self.raw_data, self.g_link)
            self.score_tot.append(dimension_score)
            self.final_list.append(dimension[0].dim_to_string())
            self.final_score += (dimension[1] * dimension_score)
            tot_weight += dimension[1]
        self.final_score = self.final_score / tot_weight

    def get_total_score(self):
        return self.final_score

    def get_complet_result(self):
        return self.final_list
