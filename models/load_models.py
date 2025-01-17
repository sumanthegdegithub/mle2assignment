import sys
import os
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from config.logger import logger

import joblib

def load_models():
    
    try:
        rf_model = joblib.load(os.path.join(str(parent),'saved_models/rf.joblib'))
        label_encoder = joblib.load(os.path.join(str(parent),'saved_models/label_encoder.joblib'))
        vectorizer = joblib.load(os.path.join(str(parent),'saved_models/vectorizer.joblib'))

        return rf_model, label_encoder, vectorizer

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log  =f'{exc_type} occured in {fname} at line {exc_tb.tb_lineno}'
        logger.info(log)

        return None, None, None