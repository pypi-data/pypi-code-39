"""
    Clase que contiene la logica de un agente
    para poder responder a las diferentes acciones
    que se le aplican.
"""
import sys
import inspect
import json
import socket
import uuid
import datetime
from abc import ABCMeta, abstractmethod # OPP
from .kafkaBase import KafkaBase
from .options import Options

class Worker(KafkaBase, metaclass=ABCMeta):

    # Acciones del microservicio
    __ACTIONS = {}

    def __init__(self, opt):
        # Validar que se pase un objeto de configuracion correcto
        if not isinstance(opt, Options):
            self.logs.error('No se proporciono una configuracion correcta')
            sys.exit(-1)

        # llamar el constructor padre
        KafkaBase.__init__(self, opt.Name, opt.Topic, opt.Kafka)
    
    def _message(self, msg):
        """
            Metodo para capturar los datos del mensaje
        """
        # Enviar al elemento que los procesa
        self.process(msg)
    
    @abstractmethod
    def process(self, data):
        pass
