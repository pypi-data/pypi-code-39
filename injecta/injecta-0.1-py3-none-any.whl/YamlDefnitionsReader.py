import yaml
from Injecta.DefinitionParser import DefinitionParser

class YamlDefnitionsReader:

    def __init__(self):
        self.__definitionParser = DefinitionParser()

    def readDefinitions(self, servicesConfigPath: str):
        with open(servicesConfigPath, 'r', encoding='utf-8') as f:
            yamlDefinitions = yaml.safe_load(f.read())
            f.close()

        return list(self.__definitionParser.parse(name, definition) for name, definition in yamlDefinitions.items())
