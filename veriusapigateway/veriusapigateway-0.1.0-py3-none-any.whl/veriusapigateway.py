import requests
import json
import logging


class VeriUsAPIGateway:

    def __init__(self, apikey):
        self.apikey = apikey
        self.headers = {'Content-Type': 'application/json', "apikey": self.apikey}
        self.function_dictionary = {
            "text-similarity": self.get_text_similarity,
            "language-detection": self.get_language,
            "abusive-content-detection": self.get_abusive,
            "text-summarization": self.get_summary,
            "keyword-extraction": self.get_keywords,
            "entity-extraction": self.get_named_entities,
            "distorted-language-detection": self.get_distorted,
            "intent-detection": self.get_intent,
            "morphological-analysis": self.get_morphology,
            "sexual-content-detection": self.get_sexual,
            "gibberish-detection": self.get_gibberish,
            "normalization": self.get_normal,
            "deasciifier": self.get_deasciified,
            "sentence-tokenizer": self.get_sentence_tokens,
            "arabic-text-summarization": self.get_arabic_summary,
            "arabic-keyword-extraction": self.get_arabic_keywords,
            "arabic-sentiment-classification": self.get_arabic_sentiment,
            "arabic-news-classification": self.get_arabic_news_class,
            "turkish-stemmer": self.get_stem,
            "sentiment-analysis": self.get_sentiment,
            "sentiment-classification": self.get_sentiment,
            "topic-detection": self.get_topics
        }

    def __post_to_access(self, endpoint, text1, text2=None):

        if text1 and text2:
            data = {"text1": text1, "text2": text2}

        elif text1:
            data = {"text": text1}
        else:
            result = {"result": None, "confidency": None, "message": "Please enter a text."}
            return result

        try:
            response = requests.post("https://api.verius.com.tr/" + endpoint,
                                     headers=self.headers, data=json.dumps(data).encode('utf-8'))
            result = response.json()
        except Exception as e:
            logging.warning(e)
            result = {"result": None, "confidency": None, "message": "Can not reach Verius API"}

        return result

    def get_text_similarity(self, text1, text2):
        return self.__post_to_access(endpoint="text-similarity", text1=text1, text2=text2)

    def get_semantic_similarity(self, text1, text2):
        return self.__post_to_access(endpoint="semantic-similarity", text1=text1, text2=text2)

    def get_language(self, text):
        return self.__post_to_access(endpoint="language-detection", text1=text)

    def get_part_of_speech_tags(self, text):
        return self.__post_to_access(endpoint="pos-tag", text1=text)

    def get_abusive(self, text):
        return self.__post_to_access(endpoint="abusive-content-detection/abusive-content-detection", text1=text)

    def get_summary(self, text):
        return self.__post_to_access(endpoint="text-summarizer", text1=text)

    def get_keywords(self, text):
        return self.__post_to_access(endpoint="keyword-extractor", text1=text)

    def get_named_entities(self, text):
        return self.__post_to_access(endpoint="entity-extraction", text1=text)

    def get_distorted(self, text):
        return self.__post_to_access(endpoint="distorted-language-detection", text1=text)

    def get_intent(self, text):
        return self.__post_to_access(endpoint="intent-detection", text1=text)

    def get_news_class(self, text):
        return self.__post_to_access(endpoint="news-classification", text1=text)

    def get_product_category(self, text):
        return self.__post_to_access(endpoint="product-category-classification", text1=text)

    def get_morphology(self, text):
        return self.__post_to_access(endpoint="morphology", text1=text)

    def get_sexual(self, text):
        return self.__post_to_access(endpoint="sexual-content-detection", text1=text)

    def get_gibberish(self, text):
        return self.__post_to_access(endpoint="gibberish-detection", text1=text)

    def get_normal(self, text):
        return self.__post_to_access(endpoint="normalization/normalization", text1=text)

    def get_deasciified(self, text):
        return self.__post_to_access(endpoint="deasciifier/deasciifier", text1=text)

    def get_sentence_tokens(self, text):
        return self.__post_to_access(endpoint="sentence-tokenizer", text1=text)

    def get_sentiment(self, text):
        return self.__post_to_access(endpoint="sentiment-analysis/sentiment-analysis", text1=text)

    def get_arabic_sentiment(self, text):
        return self.__post_to_access(endpoint="sentiment-analysis-arabic", text1=text)

    def get_arabic_news_class(self, text):
        return self.__post_to_access(endpoint="arabic-news-classification", text1=text)

    def get_stem(self, text):
        return self.__post_to_access(endpoint="stemmer", text1=text)

    def get_arabic_summary(self, text):
        return self.__post_to_access(endpoint="arabic-text-summarizer", text1=text)

    def get_topics(self, text):
        return self.__post_to_access(endpoint="topic-detection", text1=text)

    def get_arabic_keywords(self, text):
        return self.__post_to_access(endpoint="arabic-keyword-extractor", text1=text)
