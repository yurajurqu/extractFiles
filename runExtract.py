import logging
logging.basicConfig(filename='extractEntry.log',level=logging.DEBUG)
import sys
import extract
if len(sys.argv)>=3:
    parts = sys.argv[1:]
    directory = " ".join(parts)
else:
    directory = sys.argv[1]
logging.info("Directory: "+ directory)
logging.info(sys.argv)
extract.extractZipsFromCurrentDir(directory)