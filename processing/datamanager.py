import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from pypdf import PdfReader
import requests
from config.logger import logger
from io import BytesIO
import os
import sys
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def download_pdf_from_url(url:str) -> str:
    try:
        if str(url)[-3:].lower() == 'pdf':
            url = str(url)[:-3]+'pdf'
        if str(url)[:6].lower() != 'https:' and str(url)[:5].lower() != 'http:':
            url = 'https:'+url
            
        # Send the request with headers
        logger.info(url)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        pdf_file = BytesIO(response.content)
        return pdf_file
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log  =f'{exc_type} occured in {fname} at line {exc_tb.tb_lineno}'
        logger.info(log)
        return None
    
    except requests.exceptions.HTTPError as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log  =f'{exc_type} occured in {fname} at line {exc_tb.tb_lineno}'
        logger.info(log)

        return None

def pdf_to_text(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        result = ''
        for page in reader.pages:
            result += page.extract_text()
        return result
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log  =f'{exc_type} occured in {fname} at line {exc_tb.tb_lineno}'
        logger.info(log)
        return None
    
def text_preprocessor(text):

    try:
        text = text.lower()
        text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
        text = re.sub(r"[^a-z\s]", '', text)
        words = word_tokenize(text)
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        return " ".join(words)
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log  =f'{exc_type} occured in {fname} at line {exc_tb.tb_lineno}'
        logger.info(log)
        return None