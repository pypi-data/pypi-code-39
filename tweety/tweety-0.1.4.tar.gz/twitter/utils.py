# Load library
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from selenium.webdriver.chrome.options import Options
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from selenium import webdriver
from textblob import TextBlob
from bs4 import BeautifulSoup
from datetime import datetime
import chromedriver_binary
from requests import get
import pandas as pd
import time
import nltk
import sys
import re
# You will have to download the set of stop words the first time
nltk.download('stopwords')
