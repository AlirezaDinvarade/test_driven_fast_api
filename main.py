from fastapi import FastAPI
import logging
import logging.config


# logging.basicConfig(level=logging.DEBUG)
logging.config.fileConfig("logging.conf", disable_existing_loggers=False, filename='dev.log')
logger = logging.getLogger(__name__)


app = FastAPI()




