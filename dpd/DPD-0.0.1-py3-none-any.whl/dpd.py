import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile
from os.path import join
from gensim.models.doc2vec import Doc2Vec
from gensim.models import Word2Vec
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from .util import tokenize_text
from .util import STOP_WORDS_SPANISH
from .util import W2V_STD_PARAMS
from .util import STD_CLUSTERING
from .util import STD_CLUSTERING_PARAMS
from .util import STD_DENDROGRAM_METHOD
from .util import STD_DISTANCE

class dpd_generator:
	def __init__(self):
		self.corpus = []

	def build_corpus(self, folder_path, replace=True):
		"""
		Load and tokenize the sentences of a set of discourses

		Args:
			folder_path (str): path to the discourses folder
			replace (bool): If replace is True the new corpus replaces the old
				one, otherwise the new corpus is appended to the old one
		"""
		sentences = []
		for fn in listdir(folder_path):
			path_fn = join(folder_path, fn)
			if isfile(path_fn) and fn[0] != ".":
				f = open(path_fn, "r").read()
				sentences += tokenize_text(f)
		if replace:
			self.corpus = sentences
		else:
			self.corpus += sentences

	def filter_stop_words(self, stop_words = STOP_WORDS_SPANISH):
		"""
		Remove stop words from corpus

		Args:
			stop_words (list): list of stop words

		"""
		clean_corpus = []
		for sentence in self.corpus:
			clean_sentence = [w for w in sentence if w not in stop_words]
			clean_corpus.append(clean_sentence)
		self.corpus = clean_corpus


	def build_vector_space_model(self, w2v_params = W2V_STD_PARAMS):
		"""
		Trains a Word2Vec word embedding algorithm and gets the vector space model

		Args:
			w2v_params (dict): gensim.Word2Vec parameters dictionnary

		"""
		self.w2v_model = Word2Vec(**W2V_STD_PARAMS)
		self.w2v_model.build_vocab(self.corpus, progress_per=10000)
		self.w2v_model.train(self.corpus,
							 total_examples=self.w2v_model.corpus_count,
							 epochs=w2v_params["iter"],
							 report_delay=1)
		self.word_vectors = pd.DataFrame(self.w2v_model.wv.vectors,
										index=self.w2v_model.wv.vocab.keys())
		self.frequency = pd.Series({w: self.w2v_model.wv.vocab[w].count for w in self.word_vectors.index})

	def build_clusters(self,
					  clutering_constructor=STD_CLUSTERING,
					  clustering_params=STD_CLUSTERING_PARAMS):
		"""
		Apply a clustering algorithm to partition word vector representations

		Args:
			clutering_constructor (func): clustering method constructor
				the clustering method should have a fit and a predict function
				as in scikit-learn

			clustering_params (dict): parameters for the clustering constructor

		"""
		self.clustering_algorithm = clutering_constructor(**clustering_params)
		self.clustering_algorithm.fit(self.word_vectors)
		self.clustering = self.clustering_algorithm.predict(self.word_vectors)
		self.clustering = pd.Series(self.clustering,
									index=self.word_vectors.index)
		print(self.clustering)

	def build_dendrograms(self,
						  output_folder,
						  method=STD_DENDROGRAM_METHOD,
						  distance=STD_DISTANCE):
		"""
		Build a dendrogram for each cluster

		Args:
			output_folder (str): folder to output figures
			method (str): hierarchical clustering method to compute dendrogram
				using scipy.cluster.hierarchy
			distance (str): distance to compute dendrogram using
				scipy.cluster.hierarchy

		"""
		word_vectors = self.word_vectors.copy()
		word_vectors["cluster"] = self.clustering
		gb = word_vectors.groupby("cluster")
		for cluster in gb.groups.keys():
			cluster_word_vectors = gb.get_group(cluster)
			del cluster_word_vectors["cluster"]
			frequencies = self.frequency[cluster_word_vectors.index]
			Z = hierarchy.linkage(cluster_word_vectors,
								  method,
								  metric=distance)
			labels = [str(w)+":"+str(c) for w,c in frequencies.iteritems()]
			height =  max(int(np.ceil(len(frequencies.index)*50*1./700)),6)
			fig = plt.figure(figsize=(6, height))
			dendrogram(Z,
					   labels=labels,
					   orientation="right",
					   leaf_font_size=6,
					   count_sort="ascending")
			plt.tight_layout()
			file_name = str(int(cluster))+"_"+method+"_"+distance+".pdf"
			plt.savefig(join(output_folder,file_name))
