import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"       # what is the name of the file it will ensure

log_path=os.path.join(os.getcwd(),"logs")      # path for file for logs

os.makedirs(log_path,exist_ok=True)                     # creating file for logs

LOG_FILEPATH=os.path.join(log_path,LOG_FILE)              # it will combine directory and file 


logging.basicConfig(level=logging.INFO,                       # it will config of file and directory
                    filename=LOG_FILEPATH,
                    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
                    
)               # format = [2024-01-10 15:57:26,997] 6 root - INFO -  this my second tesgting