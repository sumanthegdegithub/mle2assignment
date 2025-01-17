from pypdf import PdfReader
import requests
from logger import logger
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
pdf_files_saved = os.listdir('pdf_files')

def download_pdf_from_url(url:str, save_path) -> str:
    try:
        if str(url)[-3:].lower() == 'pdf':
            url = str(url)[:-3]+'pdf'
        if str(url)[:6].lower() != 'https:' and str(url)[:5].lower() != 'http:':
            url = 'https:'+url
        
        if save_path[10:] in pdf_files_saved:
            pdf_file = save_path

        else:
            # Send the request with headers
            logger.info(url)
            response = requests.get(url, headers=headers, timeout=1)
            response.raise_for_status()
            pdf_file = BytesIO(response.content)
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
        return save_path
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
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r"[^a-z\s]", '', text)
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)

def call_api(url):
    resp = requests.get(url='http://localhost:8001/predict', params={'url':url})
    return resp.text