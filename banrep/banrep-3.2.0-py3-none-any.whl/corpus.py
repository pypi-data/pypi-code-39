# coding: utf-8
"""Módulo para crear corpus de documentos."""

from gensim.corpora import Dictionary
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Span, Token
import pandas as pd


class MiCorpus:
    """Colección de documentos."""

    def __init__(
        self,
        lang,
        datos,
        filtros=None,
        ngrams=None,
        id2word=None,
        wordlists=None,
        express=None,
        corta=0,
        no_above=0.75,
    ):
        self.lang = lang
        self.datos = datos
        self.filtros = filtros
        self.ngrams = ngrams
        self.id2word = id2word
        self.wordlists = wordlists
        self.express = express
        self.corta = corta
        self.no_above = no_above

        self.exts_doc = []
        self.exts_span = []
        self.exts_token = []

        self.fijar_extensiones()
        self.fijar_pipes()

        self.docs = [doc for doc in self.crear_docs(datos)]
        print(f"{self.__len__()} docs procesados...")

        if not self.ngrams:
            self.ngrams = self.model_ngrams()
            print("Modelo de n-gramas ha sido creado...")

        if not self.id2word:
            self.id2word = self.crear_id2word()
            print(f"Diccionario con {len(self.id2word)} términos creado...")

        self.matcher = None
        if self.express:
            self.matcher = self.crear_matcher()

    def __repr__(self):
        return f"Corpus: {self.__len__()} docs y {len(self.id2word)} términos."

    def __len__(self):
        return len(self.docs)

    def __iter__(self):
        """Iterar devuelve las palabras de cada documento como BOW."""
        for palabras in self.obtener_palabras():
            yield self.id2word.doc2bow(palabras)

    def fijar_extensiones(self):
        """Fijar extensiones globalmente."""
        if not Span.has_extension("ok_span"):
            Span.set_extension("ok_span", getter=lambda x: len(x) > self.corta)
            if "ok_span" not in self.exts_span:
                self.exts_span.append("ok_span")

        if not Token.has_extension("ok_token"):
            Token.set_extension("ok_token", default=True)
            if "ok_token" not in self.exts_token:
                self.exts_token.append("ok_token")

        if self.wordlists:
            for tipo in self.wordlists:
                if not Token.has_extension(tipo):
                    Token.set_extension(tipo, default=False)
                    if tipo not in self.exts_token:
                        self.exts_token.append(tipo)

    def fijar_pipes(self):
        if not self.lang.has_pipe("evaluar_tokens"):
            self.lang.add_pipe(self.evaluar_tokens, name="evaluar_tokens", last=True)

        if self.wordlists:
            if not self.lang.has_pipe("tokens_presentes"):
                self.lang.add_pipe(
                    self.tokens_presentes, name="tokens_presentes", last=True
                )

    def evaluar_tokens(self, doc):
        """Cambia el valor de la extension cumple (Token) si falla filtros.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        doc : spacy.tokens.Doc
        """
        for token in doc:
            if not self.token_cumple(token, filtros=self.filtros):
                token._.set("ok_token", False)

        return doc

    def tokens_presentes(self, doc):
        """Cambia valor de extensiones creadas (Token) en caso de wordlists.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        spacy.tokens.Doc
        """
        listas = self.wordlists
        if listas:
            for tipo in listas:
                wordlist = listas.get(tipo)
                for token in doc:
                    if token.lower_ in wordlist:
                        token._.set(tipo, True)

        return doc

    def crear_docs(self, datos):
        """Crea documentos a partir de textos y su metadata.

        Parameters
        ----------
        datos : Iterable[Tuple(str, dict)]
            Texto y Metadata de cada documento.

        Yields
        ------
        spacy.tokens.Doc
        """
        for doc, meta in self.lang.pipe(datos, as_tuples=True):
            for ext in meta.keys():
                if not Doc.has_extension(ext):
                    Doc.set_extension(ext, default=None)
                    if ext not in self.exts_doc:
                        self.exts_doc.append(ext)
                if meta.get(ext):
                    doc._.set(ext, meta.get(ext))

            yield doc

    def crear_matcher(self):
        """Crea PhraseMatcher para encontrar expresiones en documentos."""
        matcher = PhraseMatcher(self.lang.vocab)

        if self.express:
            for tipo in self.express:
                patterns = list(self.lang.pipe(self.express.get(tipo)))
                matcher.add(tipo, None, *patterns)

        return matcher

    def cambiar_entities(self, doc):
        """Reemplaza entities en doc basado en expresiones identificadas.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        spacy.tokens.Doc
        """
        entities = []

        if self.express:
            for match_id, start, end in self.matcher(doc):
                span = Span(doc, start, end, label=self.lang.vocab.strings[match_id])
                entities.append(span)

            doc.ents = entities

        return doc

    @staticmethod
    def frases_doc(doc):
        """Desagrega documento en frases compuestas por palabras que cumplen.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        list[list(spacy.tokens.Token)]
            Palabras de cada frase en documento.
        """
        frases = []
        for sent in doc.sents:
            if sent._.get("ok_span"):
                tokens = [tok for tok in sent if tok._.get("ok_token")]
                frases.append(tokens)

        return frases

    def iterar_frases(self):
        """Itera todas las frases del corpus.

        Yields
        ------
        Iterable[list(str)]
            Palabras de una frase.
        """
        for doc in self.docs:
            for frase in self.frases_doc(doc):
                yield [tok.lower_ for tok in frase]

    def model_ngrams(self):
        """Crea modelos de ngramas a partir de frases.

        Returns
        -------
        dict
            Modelos Phraser para bigramas y trigramas
        """
        mc = 20
        big = Phrases(self.iterar_frases(), min_count=mc)
        bigrams = Phraser(big)

        trig = Phrases(bigrams[self.iterar_frases()], min_count=mc)
        trigrams = Phraser(trig)

        return dict(bigrams=bigrams, trigrams=trigrams)

    def ngram_frases(self, doc):
        """Frases palabras de un documento, ya con ngramas.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        list[list(str)]
        """
        bigrams = self.ngrams.get("bigrams")
        trigrams = self.ngrams.get("trigrams")

        doc_ = self.frases_doc(doc)
        frases = []
        for frase in doc_:
            frases.append(list(trigrams[bigrams[[t.lower_ for t in frase]]]))

        return frases

    def obtener_palabras(self):
        """Palabras de cada documento, ya con ngramas.

        Yields
        ------
        Iterable[list(str)]
            Palabras de un documento.
        """
        for doc in self.docs:
            frases = self.ngram_frases(doc)
            palabras = [token for frase in frases for token in frase]

            yield palabras

    def crear_id2word(self):
        """Crea diccionario de todas las palabras procesadas del corpus.

        Returns
        -------
        gensim.corpora.dictionary.Dictionary
            Diccionario de todas las palabras procesas y filtradas.
        """
        id2word = Dictionary(palabras for palabras in self.obtener_palabras())
        id2word.filter_extremes(no_below=5, no_above=self.no_above)
        id2word.compactify()

        return id2word

    @staticmethod
    def token_cumple(token, filtros=None):
        """Determina si token pasa los filtros.

        Parameters
        ----------
        token : spacy.tokens.Token
            Token a evaluar.
        filtros : dict, optional
            (is_alpha, stopwords, postags, entities, chars)

        Returns
        -------
        bool
            Si token pasa los filtros o no.
        """
        if not filtros:
            return True

        stopwords = filtros.get("stopwords")
        postags = filtros.get("postags")
        entities = filtros.get("entities")
        chars = filtros.get("chars", 0)

        cumple = True if not filtros.get("is_alpha") else token.is_alpha
        if cumple:
            cumple = len(token) > chars
        if cumple:
            cumple = True if not stopwords else token.lower_ not in stopwords
        if cumple:
            cumple = True if not postags else token.pos_ not in postags
        if cumple:
            cumple = True if not entities else token.ent_type_ not in entities

        return cumple

    def corpus_stats(self):
        """Estadísticas del corpus.

        Returns
        -------
        pd.DataFrame
            Estadísticas de cada documento del corpus.
        """
        cols = self.exts_doc + self.exts_span + self.exts_token
        if self.express:
            tipos = list(self.express.keys())
            cols = cols + tipos

        data = []
        for doc in self.docs:
            fila = [doc._.get(ext) for ext in self.exts_doc]
            for ext in self.exts_span:
                fila.append(sum(sent._.get(ext) for sent in doc.sents))
            for ext in self.exts_token:
                fila.append(sum(tok._.get(ext) for tok in doc))

            if self.express:
                doc = self.cambiar_entities(doc)
                for tipo in tipos:
                    fila.append(any(ent.label_ == tipo for ent in doc.ents))

            data.append(fila)

        return pd.DataFrame(data=data, columns=cols)

    def corpus_tokens(self):
        """Tokens del corpus.

        Returns
        -------
        pd.DataFrame
            Estadisticas de cada token del corpus.
        """
        cols = ["doc_id", "sent_id", "tok_id", "word", "pos"]
        columnas = cols + self.exts_token

        items = []
        for doc in self.docs:
            sent_id = 1

            for frase in self.frases_doc(doc):
                tok_id = 1
                for tok in frase:
                    fila = [doc._.get("doc_id"), sent_id, tok_id, tok.lower_, tok.pos_]
                    for ext in self.exts_token:
                        fila.append(tok._.get(ext))
                    tok_id += 1

                    items.append(fila)

                sent_id += 1

        return pd.DataFrame(items, columns=columnas)

    def corpus_ngramed(self):
        """Tokens del corpus con ngramas.

        Returns
        -------
        pd.DataFrame
            Estadisticas de cada token del corpus.
        """
        columnas = ["doc_id", "sent_id", "tok_id", "word"]

        items = []
        for doc in self.docs:
            sent_id = 1

            for frase in self.ngram_frases(doc):
                tok_id = 1
                for tok in frase:
                    fila = [doc._.get("doc_id"), sent_id, tok_id, tok]
                    tok_id += 1

                    items.append(fila)

                sent_id += 1

        return pd.DataFrame(items, columns=columnas)

    def frases_stats(self):
        """Estadísticas de frases.

        Returns
        -------
        pd.DataFrame
            Estadísticas de cada frase del corpus.
        """
        cols = ["doc_id", "sent_id", "frase"]
        columnas = cols + self.exts_span + self.exts_token
        if self.express:
            tipos = list(self.express.keys())
            columnas = columnas + tipos

        items = []
        for doc in self.docs:
            if self.express:
                doc = self.cambiar_entities(doc)
            sent_id = 1
            for sent in doc.sents:
                fila = [doc._.get("doc_id"), sent_id, sent.text]
                for ext in self.exts_span:
                    fila.append(sent._.get(ext))
                for ext in self.exts_token:
                    fila.append(sum(tok._.get(ext) for tok in sent))

                if self.express:
                    for tipo in tipos:
                        fila.append(any(ent.label_ == tipo for ent in sent.ents))

                items.append(fila)
                sent_id += 1

        return pd.DataFrame(items, columns=columnas)
