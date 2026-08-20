import logging
import os  ## Python built-in module for recording Logs
from datetime import datetime ## for current date/time

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"  ## Get current date/time + format
logs_path = os.path.join(os.getcwd(),"logs",LOG_FILE)

## logs_path -- Variable name
## os.path.join -- To join
## os.getcwd() -- get current working directory (cwd)
## logs -- Creates Folder (logs)
## LOG_FILE -- inside logs folder, store in this FORMAT

os.makedirs(logs_path,exist_ok=True)

## os.makedirs -- Creates Folder (logs) if does not exist

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

## LOG_FILE_PATH -- Joins Folder(logs) and format file

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s" ,
    level=logging.INFO,
)

### Entry point-- to test / run this file
if __name__ == "__main__":
    logging.info("Logging File is working!")