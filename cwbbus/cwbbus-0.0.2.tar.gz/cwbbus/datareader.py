from os import makedirs, path
from typing import Union

import pandas as pd

from .filetype import FileType


class DataReader(object):
	def __init__(self):
		"""
		Stores all dataframes and provides methods to feed data into the dataframes.
		"""
		self.bus_lines = pd.DataFrame(columns=['id', 'name', 'color', 'card_only', 'category'])
		self.bus_line_shapes = pd.DataFrame(columns=['id', 'bus_line_id', 'latitude', 'longitude'])
		self.bus_stops = pd.DataFrame(columns=['number', 'name', 'type', 'latitude', 'longitude'])
		self.itineraries = pd.DataFrame(columns=['id', 'bus_line_id', 'direction'])
		self.itinerary_stops = pd.DataFrame(columns=['itinerary_id', 'sequence_number', 'stop_number'])
		self.bus_lines_schedule_tables = pd.DataFrame(columns=['table_id', 'bus_line_id', 'bus_stop_id', 'day_type',
		                                                       'time', 'adaptive'])
		self.vehicles_schedule_tables = pd.DataFrame(columns=['table_id', 'bus_line_id', 'bus_stop_id', 'vehicle_id',
		                                                      'time'])
		self.itinerary_stops_extra = pd.DataFrame(columns=['itinerary_id', 'itinerary_name', 'bus_line_id',
		                                                   'itinerary_stop_id', 'stop_name', 'stop_name_short',
		                                                   'stop_name_abbr', 'bus_stop_id', 'sequence_number', 'type',
		                                                   'special_stop'])
		self.itinerary_distances = pd.DataFrame(columns=['itinerary_stop_id', 'itinerary_next_stop_id', 'distance_m'])
		self.companies = pd.DataFrame(columns=['id', 'name'])
		self.itinerary_stops_companies = pd.DataFrame(columns=['itinerary_stop_id', 'company_id'])
		self.vehicle_log = pd.DataFrame(columns=['timestamp', 'vehicle_id', 'bus_line_id', 'latitude', 'longitude'])
		self.points_of_interest = pd.DataFrame(columns=['name', 'description', 'category', 'latitude', 'longitude'])

	def feed_data(self, file: Union[bytes, str], data_type: FileType):
		"""
		Feeds data into the reader's internal dataframes.
		:param file: File which contains the data.
		If a *bytes* object is provided, the object will be interpreted as the actual decompressed content of the file.
		Alternatively, if a *str* object is provided, the object will be interpreted as the path to a file in the user's
		operating system. Supports the same compression types supported by pandas.
		:param data_type: Type of data. See :class:`FileType` for available types
		"""
		# User provided raw binary data or file path (both are supported by pandas)
		if isinstance(file, bytes) or isinstance(file, str):
			# pd.read_json can take a long time. Therefore, we only read the file if the data_type parameter is valid.
			if data_type == FileType.LINHAS:
				file_data = pd.read_json(file)
				self._feed_linhas_json(file_data)
			elif data_type == FileType.POIS:
				file_data = pd.read_json(file)
				self._feed_pois_json(file_data)
			elif data_type == FileType.PONTOS_LINHA:
				file_data = pd.read_json(file)
				self._feed_pontos_linha_json(file_data)
			elif data_type == FileType.SHAPE_LINHA:
				file_data = pd.read_json(file)
				self._feed_shape_linha_json(file_data)
			elif data_type == FileType.TABELA_LINHA:
				file_data = pd.read_json(file)
				self._feed_tabela_linha_json(file_data)
			elif data_type == FileType.TABELA_VEICULO:
				file_data = pd.read_json(file)
				self._feed_tabela_veiculo_json(file_data)
			elif data_type == FileType.TRECHOS_ITINERARIOS:
				file_data = pd.read_json(file)
				self._feed_trechos_itinerarios_json(file_data)
			elif data_type == FileType.VEICULOS:
				file_data = pd.read_json(file, lines=True)
				self._feed_veiculos_json(file_data)
			else:
				raise ValueError("Invalid data_type parameter")

		# Unsupported type
		else:
			raise TypeError("Expected bytes (file content) or str (file name)")

	def save_dataframe_cache(self, directory_path: str):
		"""
		Dumps all data currently stored in the internal dataframes to a cache directory.
		:param directory_path: Path to the cache directory
		"""
		makedirs(directory_path, exist_ok=True)
		self.bus_lines.to_csv(path.join(directory_path, 'bus_lines.csv.xz'), index=False)
		self.bus_line_shapes.to_csv(path.join(directory_path, 'bus_lines_shapes.csv.xz'), index=False)
		self.bus_stops.to_csv(path.join(directory_path, 'bus_stops.csv.xz'), index=False)
		self.itineraries.to_csv(path.join(directory_path, 'itineraries.csv.xz'), index=False)
		self.itinerary_stops.to_csv(path.join(directory_path, 'itinerary_stops.csv.xz'), index=False)
		self.bus_lines_schedule_tables.to_csv(path.join(directory_path, 'bus_lines_schedule_tables.csv.xz'), index=False)
		self.vehicles_schedule_tables.to_csv(path.join(directory_path, 'vehicles_schedule_tables.csv.xz'), index=False)
		self.itinerary_stops_extra.to_csv(path.join(directory_path, 'itinerary_stops_extra.csv.xz'), index=False)
		self.itinerary_distances.to_csv(path.join(directory_path, 'itinerary_distances.csv.xz'), index=False)
		self.companies.to_csv(path.join(directory_path, 'companies.csv.xz'), index=False)
		self.itinerary_stops_companies.to_csv(path.join(directory_path, 'itinerary_stops_companies.csv.xz'), index=False)
		self.points_of_interest.to_csv(path.join(directory_path, 'points_of_interest.csv.xz'), index=False)
		self.vehicle_log.to_csv(path.join(directory_path, 'vehicle_log.csv.xz'), index=False)

	def from_dataframe_cache(self, directory_path: str):
		"""
		Loads all data currently stored in the specified cache directory into the internal dataframes.
		:param directory_path: Path to the cache directory
		"""
		self.bus_lines = pd.read_csv(path.join(directory_path, 'bus_lines.csv.xz'))
		self.bus_line_shapes = pd.read_csv(path.join(directory_path, 'bus_lines_shapes.csv.xz'), dtype={'bus_line_id': str})
		self.bus_stops = pd.read_csv(path.join(directory_path, 'bus_stops.csv.xz'))
		self.itineraries = pd.read_csv(path.join(directory_path, 'itineraries.csv.xz'))
		self.itinerary_stops = pd.read_csv(path.join(directory_path, 'itinerary_stops.csv.xz'))
		self.bus_lines_schedule_tables = pd.read_csv(path.join(directory_path, 'bus_lines_schedule_tables.csv.xz'))
		self.vehicles_schedule_tables = pd.read_csv(path.join(directory_path, 'vehicles_schedule_tables.csv.xz'))
		self.itinerary_stops_extra = pd.read_csv(path.join(directory_path, 'itinerary_stops_extra.csv.xz'))
		self.itinerary_distances = pd.read_csv(path.join(directory_path, 'itinerary_distances.csv.xz'))
		self.companies = pd.read_csv(path.join(directory_path, 'companies.csv.xz'))
		self.itinerary_stops_companies = pd.read_csv(path.join(directory_path, 'itinerary_stops_companies.csv.xz'))
		self.vehicle_log = pd.read_csv(path.join(directory_path, 'vehicle_log.csv.xz'))
		self.points_of_interest = pd.read_csv(path.join(directory_path, 'points_of_interest.csv.xz'))

	def _feed_linhas_json(self, file_data: pd.DataFrame):
		"""
		Merges the data provided into the bus_lines dataframe.
		:param file_data: Dataframe to merge.
		"""
		bus_line_data = file_data[['COD', 'NOME', 'NOME_COR', 'SOMENTE_CARTAO', 'CATEGORIA_SERVICO']].copy()

		bus_line_data.rename(columns={
			'COD': 'id',
			'NOME': 'name',
			'NOME_COR': 'color',
			'SOMENTE_CARTAO': 'card_only',
			"CATEGORIA_SERVICO": 'category'
		}, inplace=True)

		self.bus_lines = self.bus_lines.merge(bus_line_data, how='outer')

	def _feed_pois_json(self, file_data: pd.DataFrame):
		"""
		Merges the data provided into the points_of_interest dataframe.
		:param file_data: Dataframe to merge.
		"""
		poi_data = file_data[['POI_NAME', 'POI_DESC', 'POI_CATEGORY_NAME', 'POI_LAT', 'POI_LON']].copy()

		poi_data.rename(columns={
			'POI_NAME': 'name',
			'POI_DESC': 'description',
			'POI_CATEGORY_NAME': 'category',
			'POI_LAT': 'latitude',
			'POI_LON': 'longitude'
		}, inplace=True)

		self.points_of_interest = self.points_of_interest.merge(poi_data, how='outer')

	def _feed_pontos_linha_json(self, file_data: pd.DataFrame):
		"""
		Merges the data provided into the bus_stops, itineraries and itinerary_stops dataframes.
		:param file_data: Dataframe to merge.
		"""
		bus_stop_data = file_data[['NUM', 'NOME', 'TIPO', 'LAT', 'LON']].copy()
		itinerary_data = file_data[['ITINERARY_ID', 'COD', 'SENTIDO']].copy()
		itinerary_stops_data = file_data[['ITINERARY_ID', 'SEQ', 'NUM']].copy()

		bus_stop_data.rename(columns={
			'NUM': 'number',
			'NOME': 'name',
			'TIPO': 'type',
			'LAT': 'latitude',
			'LON': 'longitude'
		}, inplace=True)
		bus_stop_data.drop_duplicates(inplace=True)

		itinerary_data.rename(columns={
			'ITINERARY_ID': 'id',
			'COD': 'bus_line_id',
			'SENTIDO': 'direction'
		}, inplace=True)
		itinerary_data.drop_duplicates(inplace=True)

		itinerary_stops_data.rename(columns={
			'ITINERARY_ID': 'itinerary_id',
			'SEQ': 'sequence_number',
			'NUM': 'stop_number'
		}, inplace=True)
		itinerary_stops_data.drop_duplicates(inplace=True)

		self.bus_stops = self.bus_stops.merge(bus_stop_data, how='outer')
		self.itineraries = self.itineraries.merge(itinerary_data, how='outer')
		self.itinerary_stops = self.itinerary_stops.merge(itinerary_stops_data, how='outer')

	def _feed_shape_linha_json(self, file_data: pd.DataFrame):
		"""
		Merges the data provided into the bus_line_shapes dataframe.
		:param file_data: Dataframe to merge.
		"""
		bus_line_shape_data = file_data[['SHP', 'COD', 'LAT', 'LON']].copy()

		bus_line_shape_data.rename(columns={
			'SHP': 'id',
			'COD': 'bus_line_id',
			'LAT': 'latitude',
			'LON': 'longitude'
		}, inplace=True)

		self.bus_line_shapes = bus_line_shape_data

	def _feed_tabela_linha_json(self, file_data: pd.DataFrame):
		"""
		Merges the data provided into the bus_lines_schedule_tables dataframe.
		:param file_data: Dataframe to merge.
		"""
		schedule_table_data = file_data[['TABELA', 'COD', 'NUM', 'DIA', 'HORA', 'ADAPT']].copy()

		schedule_table_data.rename(columns={
			'TABELA': 'table_id',
			'COD': 'bus_line_id',
			'NUM': 'bus_stop_id',
			'DIA': 'day_type',
			'HORA': 'time',
			'ADAPT': 'adaptive'
		}, inplace=True)
		schedule_table_data.replace({'day_type': {
			1: 'weekday',
			2: 'saturday',
			3: 'sunday',
			4: 'holiday'
		}}, inplace=True)
		# TODO: Add file date to the data?

		self.bus_lines_schedule_tables = self.bus_lines_schedule_tables.merge(schedule_table_data, how='outer')

	def _feed_tabela_veiculo_json(self, file_data: pd.DataFrame):
		"""
		Merges the data provided into the vehicles_schedule_tables dataframe.
		:param file_data: Dataframe to merge.
		"""
		schedule_table_data = file_data[['TABELA', 'COD_LINHA', 'COD_PONTO', 'HORARIO', 'VEICULO']].copy()

		schedule_table_data.rename(columns={
			'TABELA': 'table_id',
			'COD_LINHA': 'bus_line_id',
			'COD_PONTO': 'bus_stop_id',
			'HORARIO': 'time',
			'VEICULO': 'vehicle_id'
		}, inplace=True)
		schedule_table_data['bus_line_id'] = schedule_table_data['bus_line_id'].astype(str)
		# TODO: Add file date to the data?

		self.vehicles_schedule_tables = self.vehicles_schedule_tables.merge(schedule_table_data, how='outer')

	def _feed_trechos_itinerarios_json(self, file_data: pd.DataFrame):
		"""
		Merges the data provided into the itinerary_stops_extra, itinerary_distances, companies and
		itinerary_stops_companies dataframes.
		:param file_data: Dataframe to merge.
		"""
		itinerary_stops_data = file_data[['COD_ITINERARIO', 'NOME_ITINERARIO', 'COD_LINHA', 'CODIGO_URBS', 'STOP_NAME',
		                                  'NOME_PTO_PARADA_TH', 'NOME_PTO_ABREVIADO', 'STOP_CODE', 'SEQ_PONTO_TRECHO_A',
		                                  'TIPO_TRECHO', 'PTO_ESPECIAL']].copy()
		itinerary_distances_data = file_data[['CODIGO_URBS', 'COD_PTO_TRECHO_B', 'EXTENSAO_TRECHO_A_ATE_B']].copy()
		company_data = file_data[['COD_EMPRESA', 'NOME_EMPRESA']].copy()
		itinerary_stops_company_data = file_data[['CODIGO_URBS', 'COD_EMPRESA']].copy()

		itinerary_stops_data.rename(columns={
			'COD_ITINERARIO': 'itinerary_id',
			'NOME_ITINERARIO': 'itinerary_name',
			'COD_LINHA': 'bus_line_id',
			'CODIGO_URBS': 'itinerary_stop_id',
			'STOP_NAME': 'stop_name',
			'NOME_PTO_PARADA_TH': 'stop_name_short',
			'NOME_PTO_ABREVIADO': 'stop_name_abbr',
			'STOP_CODE': 'bus_stop_id',
			'SEQ_PONTO_TRECHO_A': 'sequence_number',
			'TIPO_TRECHO': 'type',
			'PTO_ESPECIAL': 'special_stop'
		}, inplace=True)
		itinerary_stops_data.drop_duplicates(inplace=True)

		itinerary_distances_data.rename(columns={
			'CODIGO_URBS': 'itinerary_stop_id',
			'COD_PTO_TRECHO_B': 'itinerary_next_stop_id',
			'EXTENSAO_TRECHO_A_ATE_B': 'distance_m'
		}, inplace=True)
		itinerary_distances_data.drop_duplicates(inplace=True)

		company_data.rename(columns={
			'COD_EMPRESA': 'id',
			'NOME_EMPRESA': 'name'
		}, inplace=True)
		company_data.drop_duplicates(inplace=True)

		itinerary_stops_company_data.rename(columns={
			'CODIGO_URBS': 'itinerary_stop_id',
			'COD_EMPRESA': 'company_id'
		}, inplace=True)
		itinerary_stops_company_data.drop_duplicates(inplace=True)

		self.itinerary_stops_extra = self.itinerary_stops_extra.merge(itinerary_stops_data, how='outer')
		self.itinerary_distances = self.itinerary_distances.merge(itinerary_distances_data, how='outer')
		self.companies = self.companies.merge(company_data, how='outer')
		self.itinerary_stops_companies = self.itinerary_stops_companies.merge(itinerary_stops_company_data, how='outer')

	def _feed_veiculos_json(self, file_data: pd.DataFrame):
		"""
		Sets the data provided as the vehicle_log dataframe.
		:param file_data: Dataframe to set.
		"""
		vehicle_log_data = file_data
		vehicle_log_data.rename(columns={
			'DTHR': 'timestamp',
			'VEIC': 'vehicle_id',
			'COD_LINHA': 'bus_line_id',
			'LAT': 'latitude',
			'LON': 'longitude'
		}, inplace=True)

		vehicle_log_data['timestamp'] = pd.to_datetime(vehicle_log_data['timestamp'], format='%d/%m/%Y %H:%M:%S')

		# FIXME: these datasets are too large. How to deal with concatenation?
		# self.vehicle_log = pd.concat([self.vehicle_log, vehicle_log_data], sort=False)
		self.vehicle_log = vehicle_log_data
