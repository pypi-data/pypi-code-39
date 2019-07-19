#!/usr/bin/env python3

import pandas as pd
import mygene


mg = mygene.MyGeneInfo()


class SymbolMapping: 

	def __init__(self, symbols, symbol_type): 

		if symbol_type not in ['uniprot', 'ensemblgene']: 
			raise ValueError('symbol_type must be `uniprot` or `ensemblgene`')

		self.symbols = symbols
		self.symbol_type = symbol_type # uniprot, ensemblgene

		self.mapping = self._get_namespace_mapping()

	def _get_namespace_mapping(self): 
		"""Returns namespace mapping following a gene symbol prioritization procedure for duplicate mappings."""

		mapping = mg.querymany(self.symbols, scopes=self.symbol_type, as_dataframe=True, returnall=True)["out"]
		# Queries with duplicated gene symbols may be returned in any order, so we prioritize certain gene symbols 
		# such that gene fusions do not appear first and protein subunits are sorted alphabetically. 
		mapping['is_fusion'] = mapping.symbol.str.contains('-')
		mapping = mapping.sort_values(by=['is_fusion', 'symbol']).loc[self.symbols, 'symbol']
		return mapping

	def convert(self, df, unique_gene_symbols=False): 
		"""
		Converts input dataframe index to gene symbols.

		Arguments: 
			df (pd.DataFrame): input dataframe 
			unique_gene_symbols (bool): remove any duplicated gene symbols by keeping first instance. 

		Return:
			mapped_df (pd.DataFrame): same as `df` but indexed with gene symbols
		"""

		mapped_df = df.merge(self.mapping, left_index=True, right_index=True, how='left')

		unmapped_inputs = mapped_df.index[ mapped_df.symbol.isna() ].tolist()
		print('{} unmapped indices:'.format(len(unmapped_inputs)), unmapped_inputs)

		mapped_df = mapped_df.dropna(subset=['symbol']).set_index('symbol')

		print('Duplicated gene symbols:', mapped_df.index[mapped_df.index.duplicated(keep=False)].tolist())

		if unique_gene_symbols: 
			mapped_df = mapped_df[ ~mapped_df.index.duplicated(keep='first') ]

		return mapped_df
