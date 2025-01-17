import sys
import os
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from config.logger import logger
from processing.datamanager import download_pdf_from_url, pdf_to_text, text_preprocessor
import joblib
from config.logger import logger
from models.load_models import load_models


def inference(link:str):
    try:
        pdf_file = download_pdf_from_url(link)

        if isinstance(pdf_file, type(None)):
            raise ValueError("Unable to download pdf file from url")
        
        text = pdf_to_text(pdf_file)
        
        if isinstance(text, type(None)):
            raise ValueError("Unable to load pdf file")
        
        processed_text = text_preprocessor(text)
        
        if isinstance(processed_text, type(None)):
            raise ValueError("Unable to load text from pdf")
        
        rf_model, label_encoder, vectorizer = load_models()
        
        prediction = label_encoder.classes_[rf_model.predict(vectorizer.transform([processed_text]))[0]]
        
        class_probabilities = dict(zip(label_encoder.classes_, rf_model.predict_proba(vectorizer.transform([processed_text]))[0].tolist()))
        
        response = {'predicted_class': prediction, 'class_probabilities' : class_probabilities, 'error': None}

        return response
    
    except ValueError as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log  =f'{exc_type} occured in {fname} at line {exc_tb.tb_lineno}'
        logger.info(log)
        response = {'predicted_class': None, 'class_probabilities' : None, 'error': str(e)}
        return response
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log  =f'{exc_type} occured in {fname} at line {exc_tb.tb_lineno}'
        logger.info(log)
        error = 'Unknown error occured'
        response = {'predicted_class': None, 'class_probabilities' : None, 'error': error}
        return response



        

        
        
