from EvaMap.Dimensions.Dimension import Dimension
from EvaMap.Metrics.sameAs import sameAs
from EvaMap.Metrics.externalURIs import externalURIs
from EvaMap.Metrics.localLinks import localLinks
from EvaMap.Metrics.existingVocab import existingVocab

class Connectability(Dimension) :

    def __init__(self, nom='Connectability', list_metrics=[existingVocab, sameAs, externalURIs, localLinks]):
        super().__init__(nom, list_metrics)