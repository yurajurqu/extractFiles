import logging
logging.basicConfig(filename='extractEntry.log',level=logging.DEBUG)
import sys
import extract
directory = sys.argv[1]
logging.info("Directory: "+ directory)
logging.info(sys.argv)
extract.extractZipsFromCurrentDir(directory)