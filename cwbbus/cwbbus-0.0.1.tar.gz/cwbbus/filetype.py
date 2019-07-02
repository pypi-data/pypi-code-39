from enum import Enum, auto


class FileType(Enum):
	TRECHOS_ITINERARIOS = "trechosItinerarios.json"
	TABELA_VEICULO = "tabelaVeiculo.json"
	TABELA_LINHA = "tabelaLinha.json"
	SHAPE_LINHA = "shapeLinha.json"
	PONTOS_LINHA = "pontosLinha.json"
	POIS = "pois.json"
	LINHAS = "linhas.json"
	VEICULOS = "veiculos.json"
